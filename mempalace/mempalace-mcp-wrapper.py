#!/usr/bin/env python3
"""
MemPalace MCP Server wrapper - 替换默认 embedding 为 BGE
用法: python mempalace-mcp-wrapper.py --palace /path --bge-url http://bge:11435/v1/embeddings
"""
import sys, os, json, logging
from typing import List

logging.basicConfig(level=logging.INFO, format="[MCP-BGE] %(message)s", stream=sys.stderr)
logger = logging.getLogger("mcp-bge")

# 参数解析
args = sys.argv[1:]
palace_path = None
bge_url = None
i = 0
while i < len(args):
    if args[i] == "--palace" and i+1 < len(args):
        palace_path = os.path.abspath(args[i+1]); i += 2
    elif args[i] == "--bge-url" and i+1 < len(args):
        bge_url = args[i+1]; i += 2
    else:
        i += 1

if palace_path:
    os.environ["MEMPALACE_PALACE_PATH"] = palace_path
    logger.info(f"Palace: {palace_path}")

# BGE Embedding 函数
class BGEEmbeddingFunction:
    def __call__(self, input: List[str]) -> List[List[float]]:
        if not input: return []
        payload = json.dumps({"input": input}).encode("utf-8")
        req = __import__("urllib.request").request.Request(bge_url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
        with __import__("urllib.request").request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return [e["embedding"] for e in sorted(result["data"], key=lambda x: x["index"])]

_bge_ef = BGEEmbeddingFunction() if bge_url else None
if bge_url:
    logger.info(f"BGE embedding: {bge_url}")
else:
    logger.warning("No --bge-url, using default")

# Patch ChromaDB
import chromadb
class PatchedPC:
    def __init__(self, *a, **kw):
        self._r = chromadb.PersistentClient(*a, **kw)
    def get_or_create_collection(self, name, **kw):
        if _bge_ef and "embedding_function" not in kw: kw["embedding_function"] = _bge_ef
        return self._r.get_or_create_collection(name, **kw)
    def get_collection(self, name, **kw):
        if _bge_ef and "embedding_function" not in kw: kw["embedding_function"] = _bge_ef
        return self._r.get_collection(name, **kw)
    def __getattr__(self, n): return getattr(self._r, n)
chromadb.PersistentClient = PatchedPC
logger.info("ChromaDB patched")

# 启动 MCP
from mempalace.mcp_server import main
main()
