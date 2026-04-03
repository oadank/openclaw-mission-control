# 🔴 Mission Control i18n 危机 - 快速诊断报告

**诊断时间**: 2026-04-03 11:40 GMT+8  
**诊断者**: Critic 🎯

---

## 🚨 核心问题清单（已确认）

### 1. 无限重定向循环（致命）

**问题**: `/zh-CN` 空白页 + 网页不停刷新抖动

**根因**: `frontend/src/app/[locale]/page.tsx` 的代码：
```typescript
import { redirect } from 'next/navigation';
import { defaultLocale } from '@/i18n';

export default function Page() {
  redirect(`/${defaultLocale}`);  // ← 这里！
}
```

**问题分析**:
- 访问 `/zh-CN` → 匹配 `[locale]` 路由 → 执行 `redirect('/zh-CN')` → 再次访问 `/zh-CN` → 无限循环！

---

### 2. Clerk 认证中间件缺失（致命）

**问题**: 后台一堆报错，服务挂了

**根因**: 
- 原 `proxy.ts` 被删除了（包含完整 Clerk 认证逻辑）
- 新 `middleware.ts` 只有 next-intl，**完全没有 Clerk 认证**

**对比**:
| 原 proxy.ts | 新 middleware.ts |
|------------|-----------------|
| ✅ Clerk 认证完整 | ❌ 无 Clerk 认证 |
| ✅ 路由保护 | ❌ 无路由保护 |
| ✅ 公共路由定义 | ❌ 无公共路由 |

---

### 3. Landing 页面缺失（严重）

**问题**: 登录页是英文，根路径处理有问题

**根因**:
- 原 `app/page.tsx`（Landing 页面）被删除
- `[locale]/` 下没有对应的 Landing 页面
- 只有一个会无限重定向的 `[locale]/page.tsx`

**现状**:
- ✅ `LandingHero.tsx` 组件存在（在 `components/organisms/`）
- ❌ 没有页面文件使用它

---

### 4. 翻译键严重缺失（严重）

**问题**: 大量 UI 未汉化

**现状**:
- ✅ `en.json` 和 `zh-CN.json` 只有 `landing` 和 `dashboard` 部分
- ❌ 大量组件使用了 `useTranslations()` 但翻译键不存在

**已知缺失的翻译命名空间**:
- `sidebar` (DashboardSidebar.tsx 使用)
- `agentsPage` (agents/page.tsx 使用)
- `boardsPage` (boards/page.tsx 使用)
- `gatewaysPage` (gateways/page.tsx 使用)
- `localAuth` (LocalAuthLogin.tsx 使用)
- 还有更多...

---

## 📋 完整任务清单（待 Surveyor 细化）

### Surveyor 任务
1. ✅ Git 历史调查（已开始）
2. 🔄 完整翻译键扫描
3. 🔄 中间件对比分析
4. 🔄 路由结构完整性检查
5. 🔄 综合诊断报告

### Coder 任务（待 Surveyor 完成后）
1. 修复无限重定向循环
2. 重建集成 Clerk + next-intl 的中间件
3. 在 [locale] 下重建 Landing 页面
4. 补全所有缺失的翻译键
5. 测试所有路由和认证流程

---

## 💡 初步修复思路（仅供参考）

### 修复无限重定向
在 `[locale]/page.tsx` 渲染 LandingHero，而不是重定向

### 修复中间件
创建同时支持 next-intl 和 Clerk 的中间件（参考原 proxy.ts 中的认证逻辑）

### 修复 Landing 页面
在 `[locale]/page.tsx` 引入并渲染 `<LandingHero />`

---

**报告状态**: 初步诊断完成，等待 Surveyor 深入调查
