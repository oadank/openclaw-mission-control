# Mission Control 全面汉化执行计划

**项目位置**: `/home/node/.openclaw/workspace/openclaw-mission-control`  
**扫描时间**: 2026-04-03  
**当前汉化状态**: 部分完成

---

## 📊 扫描摘要

| 指标 | 数值 |
|------|------|
| 使用 useTranslations 的文件 | 25 个 ✅ |
| 包含硬编码英文的文件 | 67 个 ⏳ |
| 总硬编码文本命中数 | 304 处 ⏳ |
| 现有 en.json 翻译键 | 398 个 ✅ |
| 现有 zh-CN.json 翻译键 | 459 个 ✅ |

---

## 📁 涉及文件清单（按优先级）

### 🔴 Critical 优先级（3 个文件，67 处硬编码）

| 文件路径 | 硬编码数 | 主要内容 |
|---------|---------|---------|
| `src/app/[locale]/boards/[boardId]/page.tsx` | 35 | Board 详情页 ✅ **已完成** |
| `src/app/[locale]/boards/[boardId]/edit/page.tsx` | 21 | Board 编辑页（表单、选择器等） |
| `src/app/[locale]/organization/page.tsx` | 11 | 组织管理页（邀请成员、角色选择等） |

### 🟡 High 优先级（27 个文件，117 处硬编码）

| 文件路径 | 硬编码数 | 主要内容 |
|---------|---------|---------|
| `src/components/templates/LandingShell.tsx` | 30 | Landing 页导航、Footer、菜单 |
| `src/app/[locale]/board-groups/[groupId]/page.tsx` | 9 | Board 组详情页 |
| `src/components/BoardOnboardingChat.tsx` | 7 | Board 引导对话 |
| `src/app/[locale]/agents/[agentId]/page.tsx` | 6 | Agent 详情页 |
| `src/app/[locale]/skills/marketplace/page.tsx` | 6 | Skills 市场页 |
| `src/components/custom-fields/CustomFieldForm.tsx` | 6 | 自定义字段表单 |
| `src/app/[locale]/settings/page.tsx` | 5 | 设置页 |
| `src/app/[locale]/board-groups/[groupId]/edit/page.tsx` | 4 | Board 组编辑页 |
| `src/app/[locale]/board-groups/new/page.tsx` | 4 | 新建 Board 组 |
| `src/app/[locale]/boards/new/page.tsx` | 4 | 新建 Board |
| `src/app/[locale]/agents/new/page.tsx` | 3 | 新建 Agent |
| `src/app/[locale]/onboarding/page.tsx` | 3 | 引导页 |
| 其他 14 个文件 | 各 1-2 处 | 详见扫描报告 |

### 🟢 Medium 优先级（11 个文件，24 处硬编码）

主要为测试文件和较小组件。

### 🔵 Low 优先级（1 个文件，4 处硬编码）

- `src/app/[locale]/boards/[boardId]/TaskCustomFieldsEditor.tsx`

---

## 📝 需要翻译的英文文本清单（Top 50）

### 按钮与操作

| 英文文本 | 建议中文 |
|---------|---------|
| Sign in | 登录 |
| Sign In | 登录 |
| Create Account | 创建账户 |
| New task | 新建任务 |
| Edit task | 编辑任务 |
| Delete task | 删除任务 |
| Add tag | 添加标签 |
| Remove tag | 移除标签 |
| Add dependency | 添加依赖 |
| Remove dependency | 移除依赖 |
| Create board | 创建 Board |
| Edit board | 编辑 Board |
| Create board group | 创建 Board 组 |
| Edit group | 编辑组 |
| Create agent | 创建 Agent |
| Delete agent | 删除 Agent |
| Create gateway | 创建 Gateway |
| Create organization | 创建组织 |
| Create a new organization | 创建新组织 |
| Create tag | 创建标签 |
| Add custom field | 添加自定义字段 |
| Edit custom field | 编辑自定义字段 |
| Delete custom field | 删除自定义字段 |
| Delete tag | 删除标签 |
| Delete board group | 删除 Board 组 |
| Delete organization | 删除组织 |
| Remove member | 移除成员 |
| Delete your account? | 删除你的账户？ |

### 菜单与导航

| 英文文本 | 建议中文 |
|---------|---------|
| Primary navigation | 主导航 |
| OpenClaw home | OpenClaw 首页 |
| Capabilities | 功能 |
| Boards | Boards |
| Activity | 活动 |
| Gateways | Gateways |
| Dashboard | 仪表盘 |
| Agents | Agents |
| Onboarding | 引导 |
| Open Boards | 打开 Boards |
| Create Board | 创建 Board |
| Product | 产品 |
| Platform | 平台 |
| Access | 访问 |
| Board chat | Board 聊天 |
| Live feed | 实时动态 |
| Board settings | Board 设置 |
| Group chat | 组聊天 |
| Group notes | 组笔记 |
| Settings | 设置 |
| Profile | 个人资料 |

### 表单与输入

| 英文文本 | 建议中文 |
|---------|---------|
| Task title | 任务标题 |
| Task details | 任务详情 |
| Title | 标题 |
| Optional details | 可选详情 |
| Board name | Board 名称 |
| Group name | 组名称 |
| Your name | 你的姓名 |
| Enter your name | 输入你的姓名 |
| Label | 标签 |
| Tags | 标签 |
| Select status | 选择状态 |
| Select priority | 选择优先级 |
| Select gateway | 选择 Gateway |
| Select board type | 选择 Board 类型 |
| Select emoji | 选择表情 |
| Select board | 选择 Board |
| Select timezone | 选择时区 |
| Select role | 选择角色 |
| Select organization | 选择组织 |
| Select field type | 选择字段类型 |
| Select visibility | 选择可见性 |
| All categories | 所有分类 |
| All risks | 所有风险 |
| Safe | 安全 |
| No group | 无组 |
| Unassigned | 未分配 |
| Member | 成员 |
| Admin | 管理员 |
| Owner | 所有者 |
| Goal | 目标 |
| General | 通用 |
| True | 是 |
| False | 否 |
| Optional | 可选 |
| Primary gateway | 主 Gateway |
| Bearer token | Bearer 令牌 |
| Acme Robotics | Acme Robotics |
| Token | 令牌 |

### 占位符文本

| 英文文本 | 建议中文 |
|---------|---------|
| What context should the lead agent know? | 主 Agent 需要知道什么上下文？ |
| What should this board achieve? | 这个 Board 应该达成什么目标？ |
| What ties these boards together? | 是什么将这些 Boards 联系在一起？ |
| What ties these boards together? What should agents coordinate on? | 是什么将这些 Boards 联系在一起？Agents 应该协调什么？ |
| What context should the lead agent know before onboarding? | 在引导前，主 Agent 需要知道什么上下文？ |
| Describe exactly what the lead agent should do when payloads arrive. | 准确描述当 payload 到达时，主 Agent 应该做什么。 |
| Optional. Example: ^[A-Z]{3}$ | 可选。示例：^[A-Z]{3}$ |
| Optional description used by agents and UI | 供 Agents 和 UI 使用的可选描述 |
| Search boards... | 搜索 Boards... |
| Search by name, description, category, pack, source... | 按名称、描述、分类、包、来源搜索... |
| Paste invite token | 粘贴邀请令牌 |
| Type your answer... | 输入你的答案... |
| Anything else the agent should know before you confirm? (constraints, context, preferences, links, etc.) | 在确认前，Agent 还需要知道什么？（约束、上下文、偏好、链接等） |

### 提示与说明

| 英文文本 | 建议中文 |
|---------|---------|
| Lead agent (default fallback) | 主 Agent（默认后备） |
| Require approval | 需要审批 |
| Require review before done | 完成前需要审核 |
| Require comment for review | 审核需要评论 |
| Block status changes with pending approval | 有待审批时阻止状态变更 |
| Only lead can change status | 只有主 Agent 可以变更状态 |
| Board onboarding | Board 引导 |
| Close onboarding | 关闭引导 |
| Objective | 目标 |
| Success metrics | 成功指标 |
| Target date | 目标日期 |
| Board type | Board 类型 |
| Top tasks per board | 每个 Board 的首要任务 |
| Agent pace | Agent 节奏 |
| Open board | 打开 Board |
| Open task on board | 在 Board 上打开任务 |
| Close group chat | 关闭组聊天 |
| Close group notes | 关闭组笔记 |
| Close board chat | 关闭 Board 聊天 |
| Close live feed | 关闭实时动态 |
| Agent controls | Agent 控制 |
| What happens | 会发生什么 |
| Invite a member | 邀请成员 |
| Manage member access | 管理成员访问 |
| Pending | 待处理 |
| Admin only | 仅管理员 |
| No source | 无来源 |
| Install skill on gateways | 在 Gateways 上安装技能 |
| Optional description | 可选描述 |
| Toggle navigation | 切换导航 |
| Operator | 操作员 |
| OpenClaw | OpenClaw |
| Mission Control | Mission Control |
| Realtime Execution Visibility | 实时执行可见性 |
| User avatar | 用户头像 |
| Open user menu | 打开用户菜单 |
| Loading | 加载中 |
| Disable device pairing | 禁用设备配对 |
| Allow self-signed TLS certificates | 允许自签名 TLS 证书 |
| Webhook payloads | Webhook 有效载荷 |
| Skills Marketplace | 技能市场 |
| Skill Packs | 技能包 |
| Delete skill pack | 删除技能包 |
| Add skill pack | 添加技能包 |
| Custom fields | 自定义字段 |
| Board groups | Board 组 |
| Tags | 标签 |
| Heartbeat window | 心跳窗口 |
| Session binding | 会话绑定 |
| Status | 状态 |

---

## 🎯 汉化优先级排序

### Phase 1: Critical（必须先做）
1. `boards/[boardId]/page.tsx` - 35 处（核心功能页）
2. `boards/[boardId]/edit/page.tsx` - 21 处（编辑表单）
3. `organization/page.tsx` - 11 处（组织管理）

### Phase 2: High（用户可见度高）
1. `LandingShell.tsx` - 30 处（着陆页导航）
2. `board-groups/[groupId]/page.tsx` - 9 处
3. `BoardOnboardingChat.tsx` - 7 处
4. `agents/[agentId]/page.tsx` - 6 处
5. `skills/marketplace/page.tsx` - 6 处
6. `CustomFieldForm.tsx` - 6 处
7. `settings/page.tsx` - 5 处
8. 其他 High 优先级文件

### Phase 3: Medium & Low（补充完善）
- 测试文件
- 小组件
- 次要功能页

---

## 📋 执行步骤（给后续 Agent）

### Step 1: 翻译文件补充（Writer）
1. 读取现有 `messages/en.json` 和 `messages/zh-CN.json`
2. 基于上面的"需要翻译的英文文本清单"，补充缺失的翻译键
3. 统一翻译术语（Board/Agent/Gateway 保持英文或统一译法）
4. 保持 JSON 结构与现有一致

### Step 2: Critical 文件改造（Coder）
逐个处理 Critical 优先级文件：
1. 在文件顶部添加 `useTranslations()` hook
2. 将硬编码文本替换为 `t('key.path')` 调用
3. 确保翻译键在 messages 文件中存在
4. 测试页面功能正常

### Step 3: High 文件改造（Coder）
批量处理 High 优先级文件，方法同 Step 2。

### Step 4: Medium & Low 文件改造（Coder）
处理剩余文件。

### Step 5: 全面测试（Reviewer）
1. 启动开发服务器：`npm run dev`
2. 逐一测试各页面中文显示
3. 检查无英文遗漏
4. 验证功能正常

---

## 📌 注意事项

### 翻译规范
- **保持技术术语**：Board、Agent、Gateway、Dashboard 等术语建议保留英文
- **统一风格**：按钮用动词开头（"登录"而非"进行登录"）
- **简洁明了**：避免冗长，符合 UI 空间限制
- **上下文感知**：相同英文在不同上下文可能需要不同译法

### 代码规范
- 翻译键命名：使用点号分隔的层级结构，如 `board.edit.title`
- 避免硬编码：所有用户可见文本都要走 i18n
- 保持功能：修改时确保不破坏现有功能

### 现有翻译键参考
现有 `en.json` 已有 191 个键，包含：
- `common.*` - 通用
- `landing.*` - 着陆页
- `dashboard.*` - 仪表盘
- `boardsPage.*` - Boards 页
- `agentsPage.*` - Agents 页
- `gatewaysPage.*` - Gateways 页

新增键应遵循相同的命名规范。

---

**文档生成时间**: 2026-04-03  
**下一步**: 传递给 Writer 补充翻译文件，然后传递给 Coder 进行代码改造
