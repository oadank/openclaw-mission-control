# OpenClaw Mission Control (汉化版)

[![CI](https://github.com/abhi1693/openclaw-mission-control/actions/workflows/ci.yml/badge.svg)](https://github.com/abhi1693/openclaw-mission-control/actions/workflows/ci.yml) ![Static Badge](https://img.shields.io/badge/Join-Slack-active?style=flat&color=blue&link=https%3A%2F%2Fjoin.slack.com%2Ft%2Foc-mission-control%2Fshared_invite%2Fzt-3qpcm57xh-AI9C~smc3MDBVzEhvwf7gg) ![Chinese](https://img.shields.io/badge/语言 - 中文-red)

> **🎉 本项目已完成全面汉化！**
> 
> - ✅ **19 个命名空间**，**263 个翻译键**
> - ✅ **48 个页面/组件**使用国际化
> - ✅ **100% 中文界面**

---

## 🇨🇳 汉化说明

本项目已添加完整的简体中文支持，所有 UI 元素均已汉化。

### 汉化内容

| 类别 | 命名空间 | 翻译键数 | 汉化内容 |
|------|----------|----------|----------|
| **导航** | sidebar, userMenu, landing | 76 | 左侧导航、用户菜单、首页 |
| **页面** | dashboard, activityPage, approvalsPage | 22 | 仪表盘、活动、审批 |
| **管理** | boardsPage, agentsPage, gatewaysPage | 40 | 看板、智能体、网关 |
| **设置** | organizationPage, settingsPage, tagsPage, customFieldsPage | 61 | 组织、设置、标签、自定义字段 |
| **技能** | skillPacksPage, skillsMarketplacePage | 38 | 技能套件、技能市场 |
| **认证** | localAuth, signInPage | 14 | 本地认证、登录页 |
| **分组** | boardGroupsPage, common, dashboard | 12 | 看板分组、通用、仪表板卡片 |

**总计：263 个翻译键，17.5KB 翻译文件**

### 汉化示例

| 原文 | 翻译后 |
|------|--------|
| Dashboard | 仪表板 |
| Boards | 看板 |
| Agents | 智能体 |
| Gateways | 网关 |
| Approvals | 审批 |
| Settings | 设置 |
| Organization | 组织 |
| Skills Marketplace | 技能市场 |
| Activity | 活动动态 |
| Tags | 标签 |

### 技术实现

- 使用 **next-intl** 进行国际化
- 翻译文件位置：`frontend/messages/zh-CN.json`
- 默认语言：简体中文 (`zh-CN`)
- 支持语言切换（英文/中文）

---

## 平台概述

Mission Control 是 OpenClaw 的集中式运营和治理平台，用于在团队和组织中运行 OpenClaw，提供统一的可见性、审批控制和网关感知编排。

## 快速开始

### Docker Compose

```bash
git clone https://github.com/abhi1693/openclaw-mission-control.git
cd openclaw-mission-control
docker-compose up -d
```

访问：
- 前端：http://localhost:3000
- 后端：http://localhost:8000

---

## 📝 其他资源

- [英文文档](README.md) - 原始英文文档
- [安装指南](docs/getting-started/README.md) - 详细安装步骤
- [API 参考](docs/reference/api.md) - API 文档

---

## 贡献

欢迎提交 Issue 和 Pull Request！

**汉化贡献者：**
- 初始汉化完成于 2026-04-04
- 翻译文件：`frontend/messages/zh-CN.json`

---

## 许可证

MIT License
