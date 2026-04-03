# i18n 汉化覆盖率报告 - Phase 1 现状调研

**生成时间**: 2026-04-03T05:23:34.577Z
**项目**: OpenClaw Mission Control
**阶段**: Phase 1 - 现状调研

---

## 📊 概览

| 指标 | 数值 |
|------|------|
| 总 .ts/.tsx 文件数 | 416 |
| 使用 i18n 的文件数 | 8 |
| 英文翻译键总数 | 191 |
| 中文翻译键总数 | 191 |
| 代码中使用的翻译键数 | 166 |

---

## 🛣️ Next.js 路由迁移状态

### 当前状态
- **[locale] 目录存在**: ✅ 是
- **根目录中的页面数**: 0
- **[locale] 目录中的页面数**: 39

### 迁移进度
| 状态 | 数量 | 页面列表 |
|------|------|---------|
| ✅ 已迁移到 [locale] | 0 | (无) |
| ⚠️ 仅在根目录（需迁移） | 0 | (无) |
| ℹ️ 仅在 [locale] | 39 | `activity`, `agents`, `agents/[agentId]`, `agents/[agentId]/edit`, `agents/new`, `approvals`, `board-groups`, `board-groups/[groupId]`, `board-groups/[groupId]/edit`, `board-groups/new`, `boards`, `boards/[boardId]`, `boards/[boardId]/approvals`, `boards/[boardId]/edit`, `boards/[boardId]/webhooks/[webhookId]/payloads`, `boards/new`, `custom-fields`, `custom-fields/[fieldId]/edit`, `custom-fields/new`, `dashboard`, `gateways`, `gateways/[gatewayId]`, `gateways/[gatewayId]/edit`, `gateways/new`, `invite`, `onboarding`, `organization`, `settings`, `sign-in/[[...rest]]`, `skills`, `skills/marketplace`, `skills/marketplace/[skillId]/edit`, `skills/marketplace/new`, `skills/packs`, `skills/packs/[packId]/edit`, `skills/packs/new`, `tags`, `tags/[tagId]/edit`, `tags/add` |

---

## 🔑 翻译键对比

### 英文有但中文缺失的键 (0)
(无)

### 中文有但英文缺失的键 (0)
(无)

### 代码中使用但翻译文件缺失的键 (166)
- `Authorization`
- `taskId`
- `eventId`
- `signedOut`
- `title`
- `description`
- `newAgent`
- `adminOnlyMessage`
- `emptyState.title`
- `emptyState.description`
- `emptyState.actionLabel`
- `delete.ariaLabel`
- `delete.title`
- `delete.description`
- `assign_failed`
- `hidden_if_unset`
- `onboarding`
- `commentId`
- `panel`
- `.`
- `createBoard`
- `status.notConfigured`
- `status.checking`
- `status.allConnected`
- `status.partiallyConnected`
- `status.unavailable`
- `status.disconnected`
- `rows.totalWorkItems`
- `rows.inbox`
- `rows.inProgress`
- `rows.inReview`
- `rows.completed`
- `rows.completedTasks`
- `rows.averageThroughput`
- `rows.errorRate`
- `rows.completionConsistency`
- `rows.activeDays`
- `rows.reviewBacklogRatio`
- `rows.gatewayStatus`
- `rows.configuredGateways`
- `rows.connectedGateways`
- `rows.unavailableGateways`
- `rows.gatewaysWithIssues`
- `a`
- `loadFailed`
- `cards.onlineAgents`
- `cards.total`
- `cards.tasksInProgress`
- `cards.errorRate`
- `cards.completedLatest`
- `cards.completionSpeed`
- `cards.completed`
- `cards.basedOn`
- `rangeLabel`
- `sections.workload`
- `sections.throughput`
- `sections.gatewayHealth`
- `sections.pendingApprovals`
- `links.openGlobalApprovals`
- `states.loadingPendingApprovals`
- `states.pendingApprovalsUnavailable`
- `states.pendingApprovalTitle`
- `states.approvalScore`
- `states.showingPending`
- `states.noPendingApprovals`
- `sections.sessions`
- `states.noGatewaysConfigured`
- `states.loadingSessions`
- `states.gatewayUnavailable`
- `states.usageUnavailable`
- `states.activityUnavailable`
- `states.sessionDataUnavailable`
- `states.noActiveSessions`
- `sections.recentActivity`
- `links.openFeed`
- `activityAria`
- `states.noActivityYet`
- `states.activityHint`
- `createGateway`
- `token`
- `textarea`
- `redirect_url`
- `search`
- `category`
- `risk`
- `page`
- `limit`
- `packId`
- `Clarity`
- `Boom`
- `First`
- `Second`
- `Alpha`
- `Zulu`
- `Label`
- `Zara`
- `HIGH`
- `systemStatus.operational`
- `systemStatus.unavailable`
- `systemStatus.degraded`
- `navigation`
- `overview`
- `dashboard`
- `activity`
- `boards`
- `boardGroups`
- `tags`
- `approvals`
- `customFields`
- `skills`
- `marketplace`
- `packs`
- `administration`
- `organization`
- `gateways`
- `agents`
- `features.agentFirst`
- `features.approvalQueues`
- `features.liveSignals`
- `boardItems.releaseCandidate`
- `boardItems.triageApprovals`
- `boardItems.stabilizeHandoffs`
- `approvalItems.deployConfirmed`
- `approvalItems.copyReviewed`
- `approvalItems.securitySignoff`
- `signals.agentDelta`
- `signals.growthOps`
- `signals.releasePipeline`
- `featureCards.boardsTitle`
- `featureCards.boardsDescription`
- `featureCards.approvalsTitle`
- `featureCards.approvalsDescription`
- `featureCards.signalsTitle`
- `featureCards.signalsDescription`
- `featureCards.auditTitle`
- `featureCards.auditDescription`
- `openBoards`
- `viewBoards`
- `heroLabel`
- `titlePrefix`
- `titleHighlight`
- `titleSuffix`
- `commandSurface`
- `live`
- `surfaceTitle`
- `surfaceDescription`
- `metrics.boards`
- `metrics.agents`
- `metrics.tasks`
- `boardProgress`
- `approvalsPending`
- `signalsUpdated`
- `ctaTitle`
- `ctaDescription`
- `errors.tokenRequired`
- `errors.tokenLength`
- `mode`
- `subtitle`
- `tokenLabel`
- `tokenPlaceholder`
- `tokenHint`
- `validating`
- `continue`
- `2`
- `1`
- `unknown`

---

## 📁 文件级分析

### 使用 i18n 的文件 (8)
- `src/app/[locale]/agents/page.tsx` (11 个翻译键)
- `src/app/[locale]/boards/page.tsx` (10 个翻译键)
- `src/app/[locale]/dashboard/page.tsx` (59 个翻译键)
- `src/app/[locale]/gateways/page.tsx` (10 个翻译键)
- `src/components/organisms/DashboardSidebar.tsx` (19 个翻译键)
- `src/components/organisms/LandingHero.tsx` (40 个翻译键)
- `src/components/organisms/LocalAuthLogin.tsx` (10 个翻译键)
- `src/providers/NextIntlProvider.tsx` (0 个翻译键)

### 未使用 i18n 的文件 (408)
- `src/api/generated/activity/activity.ts`
- `src/api/generated/agent/agent.ts`
- `src/api/generated/agents/agents.ts`
- `src/api/generated/approvals/approvals.ts`
- `src/api/generated/auth/auth.ts`
- `src/api/generated/board-group-memory/board-group-memory.ts`
- `src/api/generated/board-groups/board-groups.ts`
- `src/api/generated/board-memory/board-memory.ts`
- `src/api/generated/board-onboarding/board-onboarding.ts`
- `src/api/generated/board-webhooks/board-webhooks.ts`
- `src/api/generated/boards/boards.ts`
- `src/api/generated/custom-fields/custom-fields.ts`
- `src/api/generated/default/default.ts`
- `src/api/generated/gateways/gateways.ts`
- `src/api/generated/health/health.ts`
- `src/api/generated/metrics/metrics.ts`
- `src/api/generated/model/activityEventRead.ts`
- `src/api/generated/model/activityEventReadRouteParams.ts`
- `src/api/generated/model/activityTaskCommentFeedItemRead.ts`
- `src/api/generated/model/agentCreate.ts`
- `src/api/generated/model/agentCreateHeartbeatConfig.ts`
- `src/api/generated/model/agentCreateIdentityProfile.ts`
- `src/api/generated/model/agentHealthStatusResponse.ts`
- `src/api/generated/model/agentHeartbeat.ts`
- `src/api/generated/model/agentHeartbeatCreate.ts`
- `src/api/generated/model/agentNudge.ts`
- `src/api/generated/model/agentRead.ts`
- `src/api/generated/model/agentReadHeartbeatConfig.ts`
- `src/api/generated/model/agentReadIdentityProfile.ts`
- `src/api/generated/model/agentUpdate.ts`
- `src/api/generated/model/agentUpdateHeartbeatConfig.ts`
- `src/api/generated/model/agentUpdateIdentityProfile.ts`
- `src/api/generated/model/approvalCreate.ts`
- `src/api/generated/model/approvalCreatePayload.ts`
- `src/api/generated/model/approvalCreateRubricScores.ts`
- `src/api/generated/model/approvalCreateStatus.ts`
- `src/api/generated/model/approvalRead.ts`
- `src/api/generated/model/approvalReadPayload.ts`
- `src/api/generated/model/approvalReadRubricScores.ts`
- `src/api/generated/model/approvalReadStatus.ts`
- `src/api/generated/model/approvalUpdate.ts`
- `src/api/generated/model/blockedTaskDetail.ts`
- `src/api/generated/model/blockedTaskError.ts`
- `src/api/generated/model/boardCreate.ts`
- `src/api/generated/model/boardCreateSuccessMetrics.ts`
- `src/api/generated/model/boardGroupBoardSnapshot.ts`
- `src/api/generated/model/boardGroupBoardSnapshotTaskCounts.ts`
- `src/api/generated/model/boardGroupCreate.ts`
- `src/api/generated/model/boardGroupHeartbeatApply.ts`
- `src/api/generated/model/boardGroupHeartbeatApplyResult.ts`
... 还有 358 个文件未列出

---

## 🎯 Phase 1 发现总结

### 🔴 关键问题
1. **路由迁移不完整**: 0 个页面仍在根目录，需要迁移到 [locale]
2. **翻译键缺失**: 166 个翻译键在代码中使用但未在翻译文件中定义
3. **部分文件未使用 i18n**: 大量 UI 组件仍可能包含硬编码英文

---

## 🚀 下一步建议（Phase 2-5）

### Phase 2: 路由修复（Coder）
1. 将 `0` 个页面从 `src/app/` 迁移到 `src/app/[locale]/`
2. 确保 layout.tsx 和 loading.tsx 正确配置
3. 验证所有内页可正常访问

### Phase 3: 翻译补全（Surveyor + Writer）
1. 补充 `166` 个缺失的翻译键
2. 统一翻译术语
3. 检查并修正已有的不恰当翻译

### Phase 4: 代码修复（Coder）
1. 扫描硬编码的英文文本，替换为 t() 调用
2. 修复缺失翻译键的组件
3. 确保所有 UI 元素都已汉化

### Phase 5: 构建与清理（Coder）
1. 运行 `npm run build`，修复构建错误
2. 整理 Git 修改

---

*Phase 1 现状调研完成*
