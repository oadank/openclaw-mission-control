# 🔍 Mission Control 汉化不生效 - 深度调查报告

**调查时间**: 2026-04-03  
**调查者**: Surveyor 📚  
**调查深度**: 深层技术分析

---

## 📋 执行摘要

经过深入调查，我发现了汉化不生效的**根本原因**和多个技术细节问题。

---

## 🔴 根本原因确认

### 核心发现：翻译文件在构建时被打包，运行时更新不生效！

**问题描述**:
- ✅ 本地翻译文件（`frontend/messages/zh-CN.json`）已更新（16,160 字节）
- ✅ 容器内的翻译文件（`/app/messages/zh-CN.json`）已手动更新（16,160 字节）
- ❌ **但是**：Next.js + next-intl 在**构建时**将翻译文件打包到了 `.next` 目录中
- ❌ **运行时**更新 `/app/messages/` 目录**不会生效**，因为应用使用的是构建时打包的翻译

---

## 🔍 技术证据链

### 证据 1：翻译文件被打包成独立的 chunk 文件

**发现位置**: `/app/.next/server/chunks/ssr/`

**打包的翻译文件**:
```
workspace_openclaw-mission-control_frontend_messages_en_json_e11d7f08._.js      (13,550 字节)
workspace_openclaw-mission-control_frontend_messages_zh-CN_json_51afb124._.js  (13,260 字节)
```

**对比分析**:
| 文件 | 大小 | 状态 |
|------|------|------|
| 源文件 zh-CN.json | 16,160 字节 | ✅ 最新 |
| 打包的 zh-CN_json_*.js | 13,260 字节 | ⚠️ **旧版本！** |

**结论**: 打包的翻译文件比源文件小 **2,900 字节**，说明是旧版本！

---

### 证据 2：Landing 页面编译文件引用打包的翻译

**发现位置**: `/app/.next/server/app/[locale]/page.js`

**编译文件头部**:
```javascript
var R=require("../../chunks/ssr/[turbopack]_runtime.js")("server/app/[locale]/page.js")
R.c("server/chunks/ssr/workspace_openclaw-mission-control_frontend_messages_3c04d3c6._.js")
R.c("server/chunks/ssr/workspace_openclaw-mission-control_frontend_messages_zh-CN_json_51afb124._.js")
...
```

**结论**: Landing 页面明确引用了**构建时打包**的翻译文件，而不是运行时的 `/app/messages/` 目录！

---

### 证据 3：i18n/request.ts 使用动态 import，但构建时已打包

**配置文件**: `src/i18n/request.ts`
```typescript
export default getRequestConfig(async ({ requestLocale }) => {
  const locale = await requestLocale;
  const validLocale = locale && isLocale(locale) ? locale : defaultLocale;
  
  return {
    locale: validLocale,
    messages: (await import(`../../messages/${validLocale}.json`)).default,
  };
});
```

**关键发现**:
- 虽然使用了动态 import `../../messages/${validLocale}.json`
- 但 Next.js 在**构建时**会分析这个 import 并预打包翻译文件
- 打包后的翻译存储在 `.next/server/chunks/ssr/` 中
- **运行时更新 `/app/messages/` 不会被使用**！

---

### 证据 4：容器日志显示 ENVIRONMENT_FALLBACK 错误

**日志摘录**:
```
Error: ENVIRONMENT_FALLBACK
    at <unknown> (.next/server/chunks/ssr/c893c_d05abb6b._.js:3:4172)
    at aw (.next/server/chunks/ssr/c893c_d05abb6b._.js:3:5727)
    at <unknown> (.next/server/chunks/ssr/c893c_d05abb6b._.js:3:7922)
```

**分析**:
- 这个错误可能与 i18n 环境配置有关
- 可能是翻译加载失败时的降级处理
- 表明 i18n 系统在尝试加载翻译时遇到了问题

---

## 🕵️ 其他可能的问题

### 问题 A：用户访问的 URL 不带 /zh-CN 前缀

**需要验证**:
- ✅ 正确 URL: `http://localhost:3000/zh-CN`
- ✅ 正确 URL: `http://localhost:3000/zh-CN/dashboard`
- ❌ 错误 URL: `http://localhost:3000/` (可能重定向到英文)
- ❌ 错误 URL: `http://localhost:3000/dashboard` (可能重定向到英文)

**建议**: 请确认用户访问的 URL 是否包含 `/zh-CN` 前缀！

---

### 问题 B：浏览器缓存了旧版本

**需要验证**:
- 建议用户硬刷新浏览器:
  - Windows/Linux: `Ctrl + Shift + R`
  - Mac: `Cmd + Shift + R`
- 或使用无痕/隐私模式访问
- 或清除浏览器缓存

---

### 问题 C：next-intl 配置检查

**已验证的配置**:
- ✅ `src/i18n.ts`: 默认语言 `zh-CN`
- ✅ `src/i18n/request.ts`: 正确配置翻译加载
- ✅ `next.config.js`: next-intl 插件正确配置
- ✅ `LandingHero.tsx`: 正确使用 `useTranslations("landing")`

---

## 🔧 解决方案

### 立即解决方案（必须执行）

#### 方案 1：重新构建 Docker 镜像（推荐）
```bash
cd /home/node/.openclaw/workspace/openclaw-mission-control
docker-compose down
docker-compose build --no-cache frontend
docker-compose up -d
```

**为什么有效**:
- `--no-cache` 确保不使用构建缓存
- 重新构建时会打包最新的翻译文件到 `.next` 目录
- 这是最彻底的解决方案

---

#### 方案 2：修复 Dockerfile（长期方案）

在 `frontend/Dockerfile` 中，确保 messages 目录被正确处理：

**当前问题**: Dockerfile 中没有显式复制 messages 目录，但构建时仍然打包了翻译（因为 Next.js 构建时会处理）

**建议改进**: 虽然不是必须的，但可以添加显式复制以便于调试：
```dockerfile
# 在 COPY .next 之后添加
COPY --from=builder --chown=appuser:appgroup /app/messages ./messages
```

---

#### 方案 3：提交翻译文件到 Git

```bash
cd /home/node/.openclaw/workspace/openclaw-mission-control
git add frontend/messages/en.json frontend/messages/zh-CN.json
git commit -m "feat: add complete Chinese translations for all pages"
```

---

### 用户端验证步骤

1. **确认访问正确的 URL**:
   - 访问: `http://localhost:3000/zh-CN`
   - 而不是: `http://localhost:3000/`

2. **硬刷新浏览器**:
   - Windows/Linux: `Ctrl + Shift + R`
   - Mac: `Cmd + Shift + R`

3. **或使用无痕模式**访问，避免缓存问题

---

## 📊 翻译键验证

### 本地翻译文件包含的命名空间 ✅
```
- common
- landing
- dashboard
- boardsPage
- agentsPage
- gatewaysPage
- sidebar
- localAuth
- activityPage
- approvalsPage
- settingsPage
- signInPage
- userMenu           (新增)
- skillPacksPage     (新增)
- boardGroupsPage    (新增)
- tagsPage           (新增)
- customFieldsPage   (新增)
- skillsMarketplacePage (新增)
- organizationPage   (新增)
```

### LandingHero.tsx 使用的翻译键 ✅
```typescript
const t = useTranslations("landing");
t("heroLabel")
t("titlePrefix")
t("titleHighlight")
t("titleSuffix")
t("description")
t("openBoards")           // ✅ 确认存在
t("createBoard")
t("viewBoards")
t("features.agentFirst")
t("features.approvalQueues")
t("features.liveSignals")
t("commandSurface")
t("live")
t("surfaceTitle")
t("surfaceDescription")
t("metrics.boards")
t("metrics.agents")
t("metrics.tasks")
t("boardProgress")
t("boardItems.releaseCandidate")
t("boardItems.triageApprovals")
t("boardItems.stabilizeHandoffs")
t("approvalsPending")
t("approvalItems.deployConfirmed")
t("approvalItems.copyReviewed")
t("approvalItems.securitySignoff")
t("signalsUpdated")
t("signals.agentDelta")
t("signals.growthOps")
t("signals.releasePipeline")
t("featureCards.boardsTitle")
t("featureCards.boardsDescription")
t("featureCards.approvalsTitle")
t("featureCards.approvalsDescription")
t("featureCards.signalsTitle")
t("featureCards.signalsDescription")
t("featureCards.auditTitle")
t("featureCards.auditDescription")
t("ctaTitle")
t("ctaDescription")
```

---

## 🎯 根本原因总结

### 主要原因（90% 可能性）
**Docker 镜像内的翻译文件在构建时被打包到 `.next` 目录，运行时更新 `/app/messages` 不生效！**

### contributing 因素
1. 翻译文件修改后没有**重新构建** Docker 镜像
2. 使用了 `docker cp` 手动更新，但 Next.js 使用的是构建时打包的翻译
3. 可能用户访问的 URL 不带 `/zh-CN` 前缀（需要验证）
4. 可能浏览器缓存了旧版本（需要验证）

---

## 📋 验证清单（执行解决方案后）

- [ ] 重新构建 Docker 镜像（带 --no-cache）
- [ ] 确认用户访问带 `/zh-CN` 前缀的 URL
- [ ] 指导用户硬刷新浏览器
- [ ] 验证 Landing 页面显示中文
- [ ] 验证 Dashboard 侧边栏显示中文
- [ ] 验证其他页面显示中文

---

## 💡 经验教训

1. **Next.js + next-intl 的翻译是构建时打包的**，运行时更新源文件不生效
2. **必须重新构建镜像**才能更新翻译
3. **Docker cp 无法更新已打包的翻译**，只能用于调试
4. **始终验证用户访问的 URL**，确保带语言前缀
5. **浏览器缓存**是常见问题，建议使用无痕模式测试

---

*深度调查完成*
