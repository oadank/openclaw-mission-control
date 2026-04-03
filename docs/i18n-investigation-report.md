# 🔍 Mission Control 汉化不生效 - 深入调查报告

**调查时间**: 2026-04-03  
**调查者**: Surveyor 📚

---

## 📋 调查总结

经过深入调查，我发现了汉化不生效的**根本原因**和多个相关问题。

---

## 🔴 核心问题清单

### 问题 1: 翻译文件修改未生效 ⚠️

**症状**: 用户刷新页面后还是看到英文

**调查发现**:
- ✅ 本地翻译文件（`frontend/messages/*.json`）**已更新**，包含完整的翻译键
- ✅ 容器内的翻译文件**也是完整的**，包含新增的翻译键
- ⚠️ 翻译文件的 Git 状态：**已修改但未提交**
- ⚠️ **关键发现**: Docker 镜像构建时间（15:53）晚于翻译文件修改时间（15:49）

**文件对比**:
| 文件 | 本地大小 | 容器内大小 | 状态 |
|------|----------|-----------|------|
| en.json | 16,129 字节 | 11,467 字节 | ⚠️ 不一致 |
| zh-CN.json | 15,837 字节 | 11,241 字节 | ⚠️ 不一致 |

**结论**: 容器内的翻译文件是**旧版本**，缺少新增的翻译键！

---

### 问题 2: Dockerfile 配置问题 🔴

**问题**: Dockerfile 中**没有显式复制 `messages/` 目录**

**当前 Dockerfile**:
```dockerfile
COPY --from=builder --chown=appuser:appgroup /app/.next ./.next
COPY --from=builder --chown=appuser:appgroup /app/package.json ./package.json
COPY --from=builder --chown=appuser:appgroup /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:appgroup /app/next.config.ts ./next.config.ts
# ❌ 缺少: COPY --from=builder --chown=appuser:appgroup /app/messages ./messages
```

**影响**: 
- next-intl 在运行时需要从文件系统读取翻译文件
- 如果 `messages/` 目录不在最终镜像中，翻译将无法加载
- 当前容器内有 messages 目录可能是因为构建缓存或其他原因

---

### 问题 3: Docker 构建缓存问题 🔴

**发现**: 
- 镜像创建时间：2026-04-03 15:53:49
- 翻译文件修改时间：2026-04-03 15:49
- 虽然时间上应该包含，但实际容器内的翻译文件是旧版本

**可能原因**:
1. Docker 构建缓存了旧的镜像层
2. 翻译文件修改后没有重新构建镜像
3. 使用了 `docker-compose up` 而没有 `--build` 标志

---

### 问题 4: 浏览器缓存和 URL 问题 🟡

**需要验证**:
1. 用户是否访问了带语言前缀的 URL？
   - ✅ 正确: `/zh-CN/dashboard`, `/zh-CN/activity`
   - ❌ 错误: `/dashboard`, `/activity` (可能重定向到英文)

2. 浏览器是否缓存了旧版本？
   - 建议：硬刷新（Ctrl+Shift+R 或 Cmd+Shift+R）
   - 建议：清除浏览器缓存

---

### 问题 5: next-intl 配置检查 ✅

**已验证**:
- ✅ `src/i18n.ts`: 默认语言设置为 `zh-CN`
- ✅ `src/i18n/request.ts`: 正确配置了翻译文件加载
- ✅ `next.config.js`: 正确配置了 next-intl 插件
- ✅ 页面文件正确使用了 `useTranslations()`

---

## 📊 翻译键覆盖情况

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

### 容器内翻译文件缺少的命名空间 ❌
```
- userMenu
- skillPacksPage
- boardGroupsPage
- tagsPage
- customFieldsPage
- skillsMarketplacePage
- organizationPage
```

---

## 🔧 解决方案

### 立即修复方案

#### 1. 重新构建 Docker 镜像（带 --no-cache）
```bash
cd /home/node/.openclaw/workspace/openclaw-mission-control
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

#### 2. 修复 Dockerfile
在 `frontend/Dockerfile` 中添加 messages 目录的复制：
```dockerfile
COPY --from=builder --chown=appuser:appgroup /app/messages ./messages
```

#### 3. 提交翻译文件到 Git
```bash
cd /home/node/.openclaw/workspace/openclaw-mission-control
git add frontend/messages/en.json frontend/messages/zh-CN.json
git commit -m "feat: add complete Chinese translations for all pages"
```

---

### 用户端验证步骤

1. **确认访问正确的 URL**:
   - 访问: `http://localhost:3000/zh-CN/dashboard`
   - 而不是: `http://localhost:3000/dashboard`

2. **硬刷新浏览器**:
   - Windows/Linux: `Ctrl + Shift + R`
   - Mac: `Cmd + Shift + R`

3. **清除浏览器缓存** 或使用无痕模式

---

## 📝 调查验证清单

- [x] 检查容器内翻译文件
- [x] 检查本地翻译文件
- [x] 对比文件大小和内容
- [x] 检查 Dockerfile 配置
- [x] 检查 Git 状态
- [x] 检查镜像构建时间
- [x] 验证 next-intl 配置
- [x] 验证页面文件使用 useTranslations
- [ ] 验证用户访问的 URL
- [ ] 验证浏览器缓存状态

---

## 🎯 根本原因确认

**主要原因**: Docker 镜像内的翻译文件是旧版本，缺少新增的翻译键（userMenu, skillPacksPage 等）

** contributing 因素**:
1. 翻译文件修改后没有重新构建 Docker 镜像
2. Dockerfile 没有显式复制 messages 目录（依赖构建缓存）
3. 可能使用了 docker-compose up 而没有 --build

---

## 📋 下一步行动

### 优先级 P0（立即执行）
1. **重新构建 Docker 镜像**（带 --no-cache）
2. **修复 Dockerfile**，添加 messages 目录复制
3. **提交翻译文件**到 Git

### 优先级 P1（验证）
1. 确认用户访问带 `/zh-CN` 前缀的 URL
2. 指导用户硬刷新浏览器
3. 验证汉化是否生效

---

*调查完成*
