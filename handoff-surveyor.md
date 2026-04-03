# 🚨 Mission Control i18n 危机 - Surveyor 深度调查任务

## 任务概述

**当前状态**: 服务严重故障，需要立即调查
**负责 Agent**: Surveyor 🧭
**优先级**: 🔴 紧急

---

## 问题症状

1. ❌ 访问 `/zh-CN` 是空白页，网页一直在刷新抖动
2. ❌ 登录页依然是英文
3. ❌ 后台一堆报错，服务挂了
4. ❌ 所有内页可能 404

---

## 调查目标

### 1. Git 历史调查

**任务**: 检查 i18n 迁移前后的完整变更

**执行**:
```bash
# 查看 i18n 提交及其父提交
git show 4b90358
git show 4b90358~1  # 父提交

# 查看当前状态与 i18n 前的差异
git diff 4b90358~1 HEAD
```

**输出**: `docs/git-history-analysis.md`

---

### 2. 翻译键扫描调查

**任务**: 找出所有使用 `useTranslations()` 但翻译键缺失的组件

**执行**:
1. 扫描 `frontend/src/**/*.tsx` 中所有 `useTranslations()` 调用
2. 提取所有翻译键（如 `t("sidebar.dashboard")` 中的 `sidebar.dashboard`）
3. 对比 `messages/en.json` 和 `messages/zh-CN.json`，找出缺失的键
4. 按组件分组列出所有缺失的翻译键

**输出**: `docs/missing-translation-keys.md`

---

### 3. 中间件对比调查

**任务**: 对比原 `proxy.ts` 和新 `middleware.ts`，找出缺失的认证逻辑

**文件位置**:
- 原 proxy.ts: git 历史中的 `frontend/src/proxy.ts` (从 4b90358~1 恢复)
- 新 middleware.ts: 当前 `frontend/src/middleware.ts`

**调查点**:
1. Clerk 认证逻辑是否完整？
2. 路由保护逻辑是否缺失？
3. 公共路由定义是否正确？
4. next-intl 和 Clerk 如何正确集成？

**输出**: `docs/middleware-comparison.md`

---

### 4. 路由结构调查

**任务**: 检查当前路由结构完整性

**执行**:
1. 列出 `frontend/src/app/` 和 `frontend/src/app/[locale]/` 的所有目录
2. 对比 i18n 迁移前的路由结构
3. 确认哪些页面已迁移，哪些缺失
4. 特别检查：Landing 页面、登录页、根路径处理

**输出**: `docs/routing-structure.md`

---

## 交付物清单

Surveyor 需产出以下文件：

| 文件 | 内容 | 优先级 |
|------|------|---------|
| `docs/git-history-analysis.md` | Git 历史变更分析 | 🔴 高 |
| `docs/missing-translation-keys.md` | 缺失翻译键完整清单 | 🔴 高 |
| `docs/middleware-comparison.md` | 中间件对比与恢复建议 | 🔴 高 |
| `docs/routing-structure.md` | 路由结构分析 | 🟡 中 |
| `docs/i18n-crisis-diagnosis.md` | 综合诊断报告（整合以上所有） | 🔴 高 |

---

## 时间预算

- **总时间**: 45 分钟
- **Git 历史**: 10 分钟
- **翻译键扫描**: 15 分钟
- **中间件对比**: 10 分钟
- **路由结构**: 5 分钟
- **综合报告**: 5 分钟

---

## Next Step

Surveyor 完成调查后，将结果交付给 **Coder** 进行紧急修复。

---

**任务创建时间**: 2026-04-03 11:35 GMT+8
**创建者**: Critic 🎯
