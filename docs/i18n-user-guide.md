# Mission Control 国际化（i18n）使用指南

**最后更新**: 2026-04-03  
**适用版本**: v1.0.0+  
**维护者**: OpenClaw 团队

---

## 目录

1. [概述](#概述)
2. [技术栈](#技术栈)
3. [目录结构](#目录结构)
4. [翻译文件](#翻译文件)
5. [使用方法](#使用方法)
6. [添加新功能时的翻译流程](#添加新功能时的翻译流程)
7. [常见问题](#常见问题)

---

## 概述

Mission Control 项目已完整支持国际化（i18n），当前支持以下语言：

| 语言代码 | 语言名称 | 状态 |
|---------|---------|------|
| `en`    | English | ✅ 完整 |
| `zh-CN` | 简体中文 | ✅ 完整 |

**默认语言**: `zh-CN` (简体中文)

---

## 技术栈

| 工具 | 版本 | 用途 |
|------|------|------|
| `next-intl` | 4.9.0 | 国际化核心库 |
| `next-translate` | - | ✅ 已弃用 |
| `react-intl` | - | ✅ 已弃用 |

**配置文件**: `frontend/src/i18n.ts` + `frontend/next.config.ts`

---

## 目录结构

```
frontend/
├── src/
│   ├── app/
│   │   ├── [locale]/           # ✅ 国际化路由目录（所有页面都在这里）
│   │   │   ├── page.tsx
│   │   │   ├── dashboard/
│   │   │   ├── boards/
│   │   │   ├── agents/
│   │   │   └── ...
│   │   ├── layout.tsx          # ❌ 旧版根布局（已弃用）
│   │   └── loading.tsx         # ❌ 旧版 loading（已弃用）
│   ├── components/
│   │   └── ...
│   └── i18n.ts                 # i18n 配置
├── messages/
│   ├── en.json                 # 英文翻译文件
│   └── zh-CN.json              # 中文翻译文件
└── next.config.ts              # Next.js + next-intl 配置
```

**关键目录说明**：

- `frontend/src/app/[locale]/`：所有页面都放在这里，路径前缀为语言代码（如 `/zh-CN/dashboard`）
- `frontend/messages/`：翻译文件目录，维护所有.text.json 文件

---

## 翻译文件

### 文件位置

- **英文**: `frontend/messages/en.json`
- **中文**: `frontend/messages/zh-CN.json`

### 文件结构

```json
{
  "命名空间1": {
    "键1": "英文/中文文本",
    "键2": "带参数的文本 {param}"
  },
  "命名空间2": {
    "子命名空间": {
      "键3": "嵌套文本"
    }
  }
}
```

### 当前翻译键统计

| 命名空间 | 键数量 | 状态 |
|---------|-------|------|
| `common` | 3 | ✅ |
| `landing` | 35 | ✅ |
| `dashboard` | 50 | ✅ |
| `boardsPage` | 15 | ✅ |
| `agentsPage` | 20 | ✅ |
| `gatewaysPage` | 20 | ✅ |
| `activityPage` | 5 | ✅ |
| `approvalsPage` | 10 | ✅ |
| `settingsPage` | 10 | ✅ |
| `signInPage` | 11 | ✅ |
| `sidebar` | 23 | ✅ |
| `localAuth` | 12 | ✅ |
| **总计** | **193** | ✅ |

---

## 使用方法

### 1. 在页面组件中使用 `useTranslations()`

```tsx
import { useTranslations } from 'next-intl';

export default function MyPage() {
  const t = useTranslations('dashboard');

  return (
    <div>
      <h1>{t('title')}</h1>
      <p>{t('description', { count: 5 })}</p>
    </div>
  );
}
```

### 2. 在服务端组件中使用 `getTranslations()`

```tsx
import { getTranslations } from 'next-intl/server';

export async function generateMetadata({ params: { locale } }: { params: { locale: string } }) {
  const t = await getTranslations({ locale, namespace: 'dashboard' });

  return {
    title: t('title'),
    description: t('description'),
  };
}
```

### 3. 在非 React 代码中使用 `formatMessage()`

```tsx
import { getRequestConfig } from 'next-intl/server';

export default getRequestConfig(async ({ locale }) => ({
  messages: (await import(`../../messages/${locale}.json`)).default,
}));
```

### 4. 参数化翻译

```json
// messages/en.json
{
  "dashboard": {
    "total": "{count} total",
    "completed": "{count} completed (latest)"
  }
}
```

```tsx
// 组件中使用
const t = useTranslations('dashboard');
t('total', { count: 5 });  // "5 total"
t('completed', { count: 3 });  // "3 completed (latest)"
```

### 5. 复数处理

```json
// messages/en.json
{
  "boardsPage": {
    "description": "{count, plural, =1 {1 board} other {# boards}} total."
  }
}
```

```tsx
// 组件中使用
const t = useTranslations('boardsPage');
t('description', { count: 1 });  // "1 board total."
t('description', { count: 5 });  // "5 boards total."
```

---

## 添加新功能时的翻译流程

### 步骤 1: 添加英文翻译键

1. 打开 `frontend/messages/en.json`
2. 找到对应的命名空间（或新建命名空间）
3. 添加英文翻译键

```json
{
  "newFeature": {
    "title": "New Feature Title",
    "description": "Description of the new feature.",
    "buttonText": "Get Started"
  }
}
```

### 步骤 2: 添加中文翻译

1. 打开 `frontend/messages/zh-CN.json`
2. 在对应命名空间下添加中文翻译

```json
{
  "newFeature": {
    "title": "新功能标题",
    "description": "新功能的描述。",
    "buttonText": "开始使用"
  }
}
```

### 步骤 3: 在组件中使用

```tsx
import { useTranslations } from 'next-intl';

export default function NewFeaturePage() {
  const t = useTranslations('newFeature');

  return (
    <div>
      <h1>{t('title')}</h1>
      <p>{t('description')}</p>
      <button>{t('buttonText')}</button>
    </div>
  );
}
```

### 步骤 4: 验证翻译

```bash
# 开发环境测试（切换语言）
# 访问 http://localhost:3000/en/new-feature
# 访问 http://localhost:3000/zh-CN/new-feature

# 构建验证
cd frontend && npm run build
```

---

## 命名空间建议

### 命名规则

1. **页面命名空间**: 使用 `pageNamePage` 格式（如 `boardsPage`、`agentsPage`）
2. **组件命名空间**: 使用 `ComponentName` 格式（如 `DashboardSidebar`）
3. **功能模块命名空间**: 使用 `camelCase` 格式（如 `newFeature`）

### 命名空间列表

| 命名空间 | 说明 | 文件位置 |
|---------|------|----------|
| `common` | 全局通用文本 | `common` |
| `landing` | Landing 页面 | `LandingHero.tsx` |
| `dashboard` | Dashboard 页面 | `dashboard/page.tsx` |
| `boardsPage` | Boards 页面 | `boards/page.tsx` |
| `agentsPage` | Agents 页面 | `agents/page.tsx` |
| `gatewaysPage` | Gateways 页面 | `gateways/page.tsx` |
| `sidebar` | 导航栏组件 | `DashboardSidebar.tsx` |
| `localAuth` | 本地认证组件 | `LocalAuthLogin.tsx` |
| `activityPage` | Activity 页面 | `activity/page.tsx` |
| `approvalsPage` | Approvals 页面 | `approvals/page.tsx` |
| `settingsPage` | Settings 页面 | `settings/page.tsx` |
| `signInPage` | Sign In 页面 | `sign-in/[[...rest]]/page.tsx` |

---

## 常见问题

### Q1: 访问路由返回 404

**问题**: 访问 `/dashboard` 等页面返回 404

**原因**: 路由未迁移到 `[locale]` 目录

**解决方案**:
1. 将页面移动到 `frontend/src/app/[locale]/` 下
2. 确保路径为 `/[locale]/dashboard` 而非 `/dashboard`

### Q2: 组件中的文本不翻译

**问题**: 组件中显示英文而非翻译后的文本

**原因**: 未使用 `useTranslations()` hook

**解决方案**:
```tsx
// ❌ 错误写法（硬编码英文）
<h1>Dashboard</h1>

// ✅ 正确写法
const t = useTranslations('dashboard');
<h1>{t('title')}</h1>
```

### Q3: 参数化翻译不生效

**问题**: `{count}` 参数未被替换

**原因**: 忘记传入参数对象

**解决方案**:
```tsx
// ❌ 错误写法
t('total');  // 返回 "{count} total"

// ✅ 正确写法
t('total', { count: 5 });  // 返回 "5 total"
```

### Q4: 中英文切换不生效

**问题**: 明明访问 `/zh-CN`，但显示英文

**原因**: i18n 配置问题

**检查清单**:
- [ ] `frontend/src/i18n.ts` 中配置了 `locale: 'zh-CN'`
- [ ] `frontend/next.config.ts` 中启用了 `next-intl`
- [ ] `messages/zh-CN.json` 文件存在且格式正确
- [ ] 页面在 `[locale]` 目录下

### Q5: 中文显示为英文或乱码

**问题**: 中文翻译显示为英文或乱码

**可能原因**:
1. `zh-CN.json` 文件编码不是 UTF-8
2. JSON 格式错误（缺少逗号、引号等）
3. 翻译键不匹配

**解决方案**:
1. 用 VS Code 打开文件，确保编码为 UTF-8
2. 用 `JSON.parse()` 验证 JSON 格式
3. 对比 `en.json` 和 `zh-CN.json` 的键结构

---

## 翻译规范

### 术语统一

| 英文 | 中文 | 说明 |
|------|------|------|
| Board | Board | 保留英文（领域术语） |
| Agent | Agent | 保留英文（领域术语） |
| Gateway | Gateway | 保留英文（领域术语） |
| Task | 任务 | 标准翻译 |
| Approval | 审批 | 标准翻译 |
| Dashboard | Dashboard | 保留英文（UI 命名） |

### 长度规范

- **按钮文本**: ≤ 10 字符（中文）或 ≤ 20 字符（英文）
- **页面标题**: ≤ 30 字符（中文）或 ≤ 50 字符（英文）
- **描述文本**: ≤ 100 字符（中文）或 ≤ 200 字符（英文）

### 大小写规范

- **标题**: 首字母大写（英文）或正常大小写（中文）
- **按钮**: 全部小写（英文）或正常大小写（中文）

---

## 维护清单

### 每次发布前

- [ ] 运行 `npm run build` 检查翻译键是否匹配
- [ ] 检查 `en.json` 和 `zh-CN.json` 的键数量是否一致
- [ ] 测试中英文切换功能
- [ ] 验证所有页面无硬编码英文

### 每次添加新功能

- [ ] 添加英文翻译键到 `en.json`
- [ ] 添加中文翻译到 `zh-CN.json`
- [ ] 在组件中使用 `useTranslations()`
- [ ] 重新构建验证

---

## 相关文档

- [Mission Control README](../README.md)
- [i18n 修复报告](./i18n-fix-report.md)
- [i18n 覆盖率报告](./i18n-coverage-report.md)

---

**维护者**: OpenClaw 团队  
**最后更新**: 2026-04-03
