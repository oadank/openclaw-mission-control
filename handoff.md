# Mission Control 汉化修复项目 - Handoff 文档

## 项目概述

**项目名称**: OpenClaw Mission Control 汉化修复  
**项目位置**: `/home/node/.openclaw/workspace/openclaw-mission-control`  
**当前状态**: 部分汉化工作已开始，但存在严重问题

---

## 问题诊断

### 主要问题

1. **🔴 所有内页报 404 错误**
   - 根由：Next.js 路由结构正在从非 i18n 迁移到 i18n 结构
   - 现象：访问 `/dashboard`, `/boards`, `/agents`, `/gateways` 等页面 404

2. **🟡 大量 UI 未汉化**
   - 登录页、菜单、按钮等仍为英文
   - 部分页面已使用 t() 函数，但翻译键缺失

3. **🔵 Git 状态混乱**
   - 大量修改未提交
   - 文件结构不完整

---

## 技术栈

- **前端**: Next.js 16.1.7 + React 19.2.4
- **国际化**: next-intl 4.9.0
- **后端**: Python (FastAPI)
- **样式**: Tailwind CSS
- **已配置语言**: `en`, `zh-CN`（默认 `zh-CN`）

---

## 任务拆解与执行计划

### Phase 1: 现状调研（Surveyor 负责）

**目标**: 全面了解当前汉化覆盖率和问题

**任务**:
1.1 扫描所有 `.tsx` 文件，统计使用 `useTranslations()` 的页面
1.2 对比 `en.json` 和 `zh-CN.json`，识别缺失的翻译键
1.3 检查 Next.js 路由结构，确认 [locale] 目录迁移状态
1.4 生成汉化覆盖率报告

**输出**: `docs/i18n-coverage-report.md`

**预估时间**: 30 分钟

---

### Phase 2: 路由修复（Coder 负责）

**目标**: 解决 404 错误，恢复所有页面访问

**任务**:
2.1 将所有路由页面从 `src/app/` 迁移到 `src/app/[locale]/`
2.2 确保 layout.tsx 和 loading.tsx 正确配置
2.3 验证所有内页可正常访问
2.4 测试语言切换功能

**依赖**: Phase 1 完成

**输出**: 可正常访问的所有页面

**预估时间**: 1 小时

**风险**: 路由迁移可能破坏现有功能 → 需充分测试

---

### Phase 3: 翻译补全（Surveyor + Writer 协作）

**目标**: 100% 汉化覆盖率

**任务**:
3.1 基于 Phase 1 的报告，补充缺失的英文翻译键到 `en.json`
3.2 将所有英文键翻译为中文，更新 `zh-CN.json`
3.3 统一翻译术语（如 Board/Agent/Gateway 的中文译法）
3.4 检查并修正已有的不恰当翻译

**依赖**: Phase 1 完成

**输出**: 完整的 `messages/en.json` 和 `messages/zh-CN.json`

**预估时间**: 1.5 小时

---

### Phase 4: 代码修复（Coder 负责）

**目标**: 确保所有 UI 文本都使用 t() 函数

**任务**:
4.1 扫描硬编码的英文文本，替换为 t() 调用
4.2 修复缺失翻译键的组件
4.3 确保登录页、菜单、按钮等所有 UI 元素都已汉化
4.4 测试所有页面的中文显示

**依赖**: Phase 2 + Phase 3 完成

**输出**: 所有页面都显示中文

**预估时间**: 1 小时

---

### Phase 5: 构建与清理（Coder 负责）

**目标**: 确保项目可正常构建，清理 Git 状态

**任务**:
5.1 运行 `npm run build`，修复构建错误
5.2 运行 `npm run lint`，修复代码风格问题
5.3 整理 Git 修改，创建清晰的 commit
5.4 清理临时文件和冗余文件

**依赖**: Phase 2-4 完成

**输出**: 
- 成功构建的项目
- 清晰的 Git 历史

**预估时间**: 45 分钟

---

## 时间线总览

| Phase | 任务 | 负责 Agent | 预估时间 | 依赖 |
|-------|------|-----------|---------|------|
| 1 | 现状调研 | Surveyor | 30 min | - |
| 2 | 路由修复 | Coder | 60 min | Phase 1 |
| 3 | 翻译补全 | Surveyor + Writer | 90 min | Phase 1 |
| 4 | 代码修复 | Coder | 60 min | Phase 2 + 3 |
| 5 | 构建与清理 | Coder | 45 min | Phase 2-4 |

**总预估时间**: 约 4.5 小时

---

## 风险评估

| 风险 | 可能性 | 影响 | 应对策略 |
|------|--------|------|---------|
| 路由迁移后部分功能失效 | 中 | 高 | 充分测试，准备回滚方案 |
| 翻译键数量远超预期 | 中 | 中 | 优先处理核心页面 |
| 构建错误难以修复 | 低 | 高 | 提前检查 package.json 依赖 |

---

## Next Step: Handoff to Surveyor

**Surveyor 任务**: 
1. 执行 Phase 1: 现状调研
2. 生成汉化覆盖率报告
3. 识别所有缺失的翻译键

**Surveyor 输入**:
- 项目位置: `/home/node/.openclaw/workspace/openclaw-mission-control`
- 当前翻译文件: `frontend/messages/en.json`, `frontend/messages/zh-CN.json`
- 前端源码: `frontend/src/`

**Surveyor 输出**:
- 覆盖率报告: `docs/i18n-coverage-report.md`
- 缺失翻译键列表

---

## 附录: 关键文件位置

| 文件 | 路径 | 说明 |
|------|------|------|
| 英文翻译 | `frontend/messages/en.json` | 英文翻译源文件 |
| 中文翻译 | `frontend/messages/zh-CN.json` | 中文翻译文件 |
| i18n 配置 | `frontend/src/i18n.ts` | 语言列表和默认语言 |
| Next.js 配置 | `frontend/next.config.ts` | next-intl 插件配置 |
| 路由目录 | `frontend/src/app/[locale]/` | 国际化路由目录 |
| 旧路由目录 | `frontend/src/app/` | 待迁移的旧路由 |

---

**文档创建时间**: 2026-04-03  
**Planner**: OpenClaw-Planner 🧠
