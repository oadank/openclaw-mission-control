#!/usr/bin/env python3
"""
Mission Control i18n 修复脚本
安全地汉化前端代码，避免破坏 import 语句和类型定义
"""

import json
import os
import re
from pathlib import Path

FRONTEND_DIR = Path("/opt/openclaw-mission-control/frontend")
MESSAGES_FILE = FRONTEND_DIR / "src" / "messages" / "zh-CN.json"
SCAN_REPORT = Path("/opt/openclaw-mission-control/i18n-scan-report.json")

# 需要翻译的硬编码文本映射（英文 -> 中文）
HARDCODED_TRANSLATIONS = {
    # 通用
    "Sign in": "登录",
    "Sign out": "退出",
    "New task": "新任务",
    "Edit task": "编辑任务",
    "Delete task": "删除任务",
    "Task title": "任务标题",
    "Task details": "任务详情",
    "Title": "标题",
    "Optional details": "可选详情",
    "Select status": "选择状态",
    "Select priority": "选择优先级",
    "Unassigned": "未分配",
    "Add tag": "添加标签",
    "Remove tag": "移除标签",
    "Add dependency": "添加依赖",
    "Remove dependency": "移除依赖",
    "Tags": "标签",
    "Priority": "优先级",
    "Status": "状态",
    "Agent controls": "Agent 控制",
    "What happens": "执行内容",
    "Approvals": "审批",
    "Board chat": "Board 聊天",
    "Live feed": "实时动态",
    "Board settings": "Board 设置",
    "Close board chat": "关闭 Board 聊天",
    "Close live feed": "关闭实时动态",
    "Settings": "设置",
    "Dashboard": "仪表盘",
    "Boards": "Boards",
    "Agents": "Agents",
    "Tasks": "任务",
    "Approve": "批准",
    "Reject": "拒绝",
    "Cancel": "取消",
    "Save": "保存",
    "Delete": "删除",
    "Edit": "编辑",
    "Create": "创建",
    "Update": "更新",
    "Loading...": "加载中...",
    "Error": "错误",
    "Success": "成功",
    "Confirm": "确认",
    "Back": "返回",
    "Next": "下一步",
    "Previous": "上一步",
    "Search": "搜索",
    "Filter": "筛选",
    "Sort": "排序",
    "Export": "导出",
    "Import": "导入",
    "Refresh": "刷新",
    "Retry": "重试",
    "Close": "关闭",
    "Open": "打开",
    "View": "查看",
    "More": "更多",
    "Less": "更少",
    "All": "全部",
    "None": "无",
    "Yes": "是",
    "No": "否",
    "OK": "确定",
    # Board 相关
    "New Board": "新 Board",
    "Edit Board": "编辑 Board",
    "Delete Board": "删除 Board",
    "Board name": "Board 名称",
    "Board description": "Board 描述",
    "Board icon": "Board 图标",
    "Board color": "Board 颜色",
    "Board owner": "Board 所有者",
    "Board members": "Board 成员",
    "Board permissions": "Board 权限",
    "Board settings": "Board 设置",
    "Board chat": "Board 聊天",
    "Board activity": "Board 活动",
    "Board analytics": "Board 分析",
    # Task 相关
    "Task": "任务",
    "Tasks": "任务",
    "Task name": "任务名称",
    "Task description": "任务描述",
    "Task assignee": "任务负责人",
    "Task reporter": "任务报告人",
    "Task priority": "任务优先级",
    "Task status": "任务状态",
    "Task due date": "任务截止日期",
    "Task created": "任务创建时间",
    "Task updated": "任务更新时间",
    "Task completed": "任务完成时间",
    # Agent 相关
    "Agent": "Agent",
    "Agent name": "Agent 名称",
    "Agent status": "Agent 状态",
    "Agent health": "Agent 健康度",
    "Agent activity": "Agent 活动",
    "Agent logs": "Agent 日志",
    "Agent settings": "Agent 设置",
    # Approval 相关
    "Approval": "审批",
    "Approvals": "审批",
    "Approval request": "审批请求",
    "Approval status": "审批状态",
    "Approval history": "审批历史",
    "Pending approvals": "待处理审批",
    "Approved": "已批准",
    "Rejected": "已拒绝",
    "Pending": "待处理",
    # 状态
    "Active": "活跃",
    "Inactive": "不活跃",
    "Online": "在线",
    "Offline": "离线",
    "Connected": "已连接",
    "Disconnected": "已断开",
    "Available": "可用",
    "Unavailable": "不可用",
    "Busy": "忙碌",
    "Idle": "空闲",
    # 时间
    "Today": "今天",
    "Yesterday": "昨天",
    "This week": "本周",
    "Last week": "上周",
    "This month": "本月",
    "Last month": "上月",
    "Recent": "最近",
    "Older": "更早",
    # 其他
    "Inbox": "收件箱",
    "In Progress": "进行中",
    "In Review": "审核中",
    "Completed": "已完成",
    "Draft": "草稿",
    "Published": "已发布",
    "Archived": "已归档",
    "Deleted": "已删除",
    "High": "高",
    "Medium": "中",
    "Low": "低",
    "Critical": "紧急",
    "Normal": "正常",
    "Urgent": "紧急",
}


def load_scan_report():
    """加载 i18n 扫描报告"""
    with open(SCAN_REPORT, "r", encoding="utf-8") as f:
        return json.load(f)


def load_messages():
    """加载现有翻译文件"""
    with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_messages(messages):
    """保存翻译文件"""
    with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)


def add_missing_keys(messages, report):
    """添加缺失的翻译 key"""
    added = 0
    
    # 从扫描报告中提取所有硬编码文本
    for file_info in report.get("filesByPriority", {}).get("critical", []):
        for hit in file_info.get("hits", []):
            text = hit.get("text", "")
            if text and text not in HARDCODED_TRANSLATIONS:
                # 生成 key
                key = text.lower().replace(" ", "_").replace("-", "_")[:30]
                # 添加到 common 或根据上下文添加
                if "common" not in messages:
                    messages["common"] = {}
                if key not in messages["common"]:
                    messages["common"][key] = text  # 暂时用英文，后续手动翻译
                    added += 1
    
    # 添加已知的翻译
    for en, zh in HARDCODED_TRANSLATIONS.items():
        key = en.lower().replace(" ", "_").replace("-", "_")[:30]
        if "common" not in messages:
            messages["common"] = {}
        if key not in messages["common"]:
            messages["common"][key] = zh
            added += 1
    
    return added


def fix_file(filepath):
    """修复单个文件的 i18n 问题"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    original = content
    changes = 0
    
    # 1. 修复重复的 useTranslations 导入
    lines = content.split("\n")
    new_lines = []
    seen_usetranslations_import = False
    skip_next = False
    
    for i, line in enumerate(lines):
        if skip_next:
            skip_next = False
            continue
        
        # 检查是否是重复的 useTranslations 导入
        if 'import { useTranslations } from "next-intl"' in line:
            if seen_usetranslations_import:
                # 跳过重复的导入
                changes += 1
                continue
            seen_usetranslations_import = True
        
        new_lines.append(line)
    
    content = "\n".join(new_lines)
    
    # 2. 替换硬编码文本（只替换 JSX 中的文本内容）
    for en, zh in HARDCODED_TRANSLATIONS.items():
        # 转义特殊字符
        en_escaped = re.escape(en)
        
        # 替换按钮文本：<Button>Text</Button>
        pattern = rf'(>)(\s*)({en_escaped})(\s*)(</(?:Button|label|span|div|p|h[1-6]|DialogTitle|DialogDescription)>)'
        match = re.search(pattern, content)
        if match:
            content = re.sub(pattern, rf'\1\2{zh}\4\5', content)
            changes += 1
        
        # 替换 aria-label
        pattern = rf'(aria-label=")({en_escaped})(")'
        if re.search(pattern, content):
            content = re.sub(pattern, rf'\1{zh}\3', content)
            changes += 1
        
        # 替换 placeholder
        pattern = rf'(placeholder=")({en_escaped})(")'
        if re.search(pattern, content):
            content = re.sub(pattern, rf'\1{zh}\3', content)
            changes += 1
        
        # 替换 title 属性
        pattern = rf'(\stitle=")({en_escaped})(")'
        if re.search(pattern, content):
            content = re.sub(pattern, rf'\1{zh}\3', content)
            changes += 1
    
    # 保存修改
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    
    return changes


def main():
    print("🔧 开始 i18n 修复...")
    
    # 1. 加载数据
    report = load_scan_report()
    messages = load_messages()
    
    print(f"📊 扫描报告：{report['summary']['totalHardcodedHits']} 处硬编码文本")
    print(f"📝 现有翻译：{len(json.dumps(messages))} 字节")
    
    # 2. 添加缺失的 key
    added = add_missing_keys(messages, report)
    save_messages(messages)
    print(f"✅ 添加 {added} 个翻译 key")
    
    # 3. 修复关键文件
    critical_files = [
        f["file"] for f in report.get("filesByPriority", {}).get("critical", [])
    ]
    
    total_changes = 0
    for rel_path in critical_files[:10]:  # 先处理前 10 个关键文件
        filepath = FRONTEND_DIR / "src" / rel_path
        if filepath.exists():
            changes = fix_file(filepath)
            if changes > 0:
                print(f"  ✏️  {rel_path}: {changes} 处修改")
                total_changes += changes
        else:
            print(f"  ⚠️  文件不存在：{rel_path}")
    
    print(f"\n✅ 完成！共修改 {total_changes} 处")
    print("📦 下一步：运行 'cd frontend && npm run build' 验证构建")


if __name__ == "__main__":
    main()
