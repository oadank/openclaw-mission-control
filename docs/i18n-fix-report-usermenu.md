# i18n 汉化修复报告 - UserMenu 组件

**修复时间**: 2026-04-03 13:30  
**修复者**: OpenClaw Assistant

---

## 问题描述

用户反馈截图显示右侧下拉菜单有大量英文未汉化：
- Open boards
- Create board
- Dashboard
- Activity
- Agents
- Gateways
- Skills marketplace
- Skill packs
- Settings
- Sign out

---

## 修复内容

### 1. 翻译文件更新

**文件**: `messages/en.json` 和 `messages/zh-CN.json`

**新增命名空间**: `userMenu`

| 键 | 英文 | 中文 |
|------|------|------|
| openBoards | Open boards | 打开看板 |
| createBoard | Create board | 创建看板 |
| dashboard | Dashboard | 仪表板 |
| activity | Activity | 活动动态 |
| agents | Agents | 智能体 |
| gateways | Gateways | 网关 |
| skillsMarketplace | Skills marketplace | 技能市场 |
| skillPacks | Skill packs | 技能套件 |
| settings | Settings | 设置 |
| signOut | Sign out | 退出登录 |

### 2. 组件代码修改

**文件**: `src/components/organisms/UserMenu.tsx`

**修改内容**:
1. 添加 `import { useTranslations } from "next-intl";`
2. 在组件内添加 `const t = useTranslations("userMenu");`
3. 替换 10 处硬编码英文为 `t()` 调用

**修改前**:
```tsx
<Link href="/boards">Open boards</Link>
<Link href="/boards/new">Create board</Link>
{item.label} // Dashboard, Activity, etc.
Sign out
```

**修改后**:
```tsx
<Link href="/boards">{t("openBoards")}</Link>
<Link href="/boards/new">{t("createBoard")}</Link>
{t("dashboard")}
{t("activity")}
// ...
{t("signOut")}
```

---

## 其他修复

### sidebar 命名空间补翻

**文件**: `messages/zh-CN.json`

修复了之前漏翻译的 4 个词：

| 键 | 修复前 | 修复后 |
|------|--------|--------|
| dashboard | Dashboard | 仪表板 |
| boards | Boards | 看板 |
| gateways | Gateways | 网关 |
| agents | Agents | 智能体 |

---

## 修改文件清单

| 文件 | 操作 |
|------|------|
| `messages/en.json` | 新增 userMenu 命名空间 |
| `messages/zh-CN.json` | 新增 userMenu 命名空间 + 修复 sidebar 漏翻 |
| `src/components/organisms/UserMenu.tsx` | 添加 i18n 支持 |

---

## 验证步骤

1. ✅ 翻译文件语法正确（JSON 格式）
2. ✅ 组件代码使用 useTranslations
3. ⏳ 需要构建并测试 UI 显示

**下一步**: 运行 `npm run build` 验证构建，然后测试 UI 显示

---

**状态**: ✅ 代码修复完成，待构建验证
