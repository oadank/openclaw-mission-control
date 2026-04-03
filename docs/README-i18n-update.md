# Mission Control 汉化修复 - README 更新

**更新内容**: 添加汉化说明章节  
**更新时间**: 2026-04-03  
**版本**: v1.0.0-i18n

---

## 更新后的 README.md

以下内容已从 README.md 中提取并更新，新增了汉化说明章节：

### 新增章节：Internationalization (i18n)

#### 🇨🇳 简体中文支持

**Mission Control 完整支持中文界面**，你可以通过以下方式切换语言：

**访问不同语言**:
- 中文界面: `http://localhost:3000/zh-CN`
- 英文界面: `http://localhost:3000/en`

**语言自动检测**: 系统会根据浏览器语言自动选择界面语言（优先级：`zh-CN` > `en`）

#### 🌍 技术栈

**国际化库**: `next-intl 4.9.0`

**支持的语言**:
| 语言代码 | 语言名称 | 状态 |
|---------|---------|------|
| `zh-CN` | 简体中文 | ✅ 完整 |
| `en`    | English | ✅ 完整 |

**翻译文件位置**:
- 英文翻译: `frontend/messages/en.json`
- 中文翻译: `frontend/messages/zh-CN.json`

#### 📚 文档

- **使用指南**: [`docs/i18n-user-guide.md`](./docs/i18n-user-guide.md)
- **修复变更日志**: [`docs/CHANGELOG-i18n.md`](./docs/CHANGELOG-i18n.md)
- **覆盖率报告**: [`docs/i18n-coverage-report.md`](./docs/i18n-coverage-report.md)

#### 🔧 开发者：添加新功能

如果你要添加新功能，需要：

1. **添加英文翻译**: 在 `frontend/messages/en.json` 中添加键值对
2. **添加中文翻译**: 在 `frontend/messages/zh-CN.json` 中添加对应的中文翻译
3. **在组件中使用**: 使用 `useTranslations()` hook 获取翻译函数

详细步骤请参考 [`docs/i18n-user-guide.md`](./docs/i18n-user-guide.md)

---

## 完整的 README.md 内容（更新后）

> **注意**: 由于 README.md 内容较长，以下只展示新增的 i18n 章节。完整内容请参考项目中的实际文件。

```
# OpenClaw Mission Control

[![CI](https://github.com/abhi1693/openclaw-mission-control/actions/workflows/ci.yml/badge.svg)](https://github.com/abhi1693/openclaw-mission-control/actions/workflows/ci.yml) ![Static Badge](https://img.shields.io/badge/Join-Slack-active?style=flat&color=blue&link=https%3A%2F%2Fjoin.slack.com%2Ft%2Foc-mission-control%2Fshared_invite%2Fzt-3qpcm57xh-AI9C~smc3MDBVzEhvwf7gg)

OpenClaw Mission Control is the centralized operations and governance platform for running OpenClaw across teams and organizations, with unified visibility, approval controls, and gateway-aware orchestration.
It gives operators a single interface for work orchestration, agent and gateway management, approval-driven governance, and API-backed automation.

...

## Internationalization (i18n)

### 🇨🇳 简体中文支持

**Mission Control 完整支持中文界面**，你可以通过以下方式切换语言：

**访问不同语言**:
- 中文界面: `http://localhost:3000/zh-CN`
- 英文界面: `http://localhost:3000/en`

**语言自动检测**: 系统会根据浏览器语言自动选择界面语言（优先级：`zh-CN` > `en`）

#### 🌍 技术栈

**国际化库**: `next-intl 4.9.0`

**支持的语言**:
| 语言代码 | 语言名称 | 状态 |
|---------|---------|------|
| `zh-CN` | 简体中文 | ✅ 完整 |
| `en`    | English | ✅ 完整 |

**翻译文件位置**:
- 英文翻译: `frontend/messages/en.json`
- 中文翻译: `frontend/messages/zh-CN.json`

#### 📚 文档

- **使用指南**: [`docs/i18n-user-guide.md`](./docs/i18n-user-guide.md)
- **修复变更日志**: [`docs/CHANGELOG-i18n.md`](./docs/CHANGELOG-i18n.md)
- **覆盖率报告**: [`docs/i18n-coverage-report.md`](./docs/i18n-coverage-report.md)

#### 🔧 开发者：添加新功能

如果你要添加新功能，需要：

1. **添加英文翻译**: 在 `frontend/messages/en.json` 中添加键值对
2. **添加中文翻译**: 在 `frontend/messages/zh-CN.json` 中添加对应的中文翻译
3. **在组件中使用**: 使用 `useTranslations()` hook 获取翻译函数

详细步骤请参考 [`docs/i18n-user-guide.md`](./docs/i18n-user-guide.md)

## Authentication

Mission Control supports two authentication modes:

- `local`: shared bearer token mode (default for self-hosted use)
- `clerk`: Clerk JWT mode

...
```

---

## 任务完成情况

| 任务 | 状态 | 说明 |
|------|------|------|
| 1. 更新 README.md 添加汉化说明 | ✅ 完成 | 新增 i18n 章节，包括语言切换方式、技术栈、文档链接和开发者指南 |
| 2. 创建 i18n 使用指南 | ✅ 完成 | `docs/i18n-user-guide.md` (7,228 字节) |
| 3. 记录本次修复的关键变更 | ✅ 完成 | `docs/CHANGELOG-i18n.md` (7,484 字节) |

---

## 交付物

| 文件 | 路径 | 大小 | 说明 |
|------|------|------|------|
| i18n 使用指南 | `docs/i18n-user-guide.md` | 7,228 字节 | 国际化使用指南，包含使用方法、命名规范、常见问题 |
| 汉化修复变更日志 | `docs/CHANGELOG-i18n.md` | 7,484 字节 | 详细的修复变更记录，包含问题描述、修复内容、验证结果 |
| 更新后的 README | `README.md` | 已更新 | 新增 i18n 章节 |

---

**任务完成时间**: 2026-04-03  
**交付人**: Writer Agent  
**下一阶段**: Monitor 验证
