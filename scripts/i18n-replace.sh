#!/bin/bash
# Mission Control i18n 安全替换脚本
# 只替换 JSX 中的硬编码文本，不破坏 import 和类型定义

set -e

FRONTEND_DIR="/opt/openclaw-mission-control/frontend"
cd "$FRONTEND_DIR"

echo "🔧 开始汉化替换..."

# 定义替换规则 (英文 -> 中文)
# 格式：sed -i 's/原内容/替换内容/g' 文件

# 关键文件列表
FILES=(
  "src/app/[locale]/boards/[boardId]/page.tsx"
  "src/app/boards/[boardId]/page.tsx"
  "src/app/[locale]/boards/[boardId]/edit/page.tsx"
  "src/app/boards/[boardId]/edit/page.tsx"
  "src/app/organization/page.tsx"
  "src/components/organisms/DashboardSidebar.tsx"
  "src/components/organisms/TaskBoard.tsx"
  "src/components/templates/DashboardShell.tsx"
)

# 通用替换函数 - 只替换 JSX 文本内容
replace_text() {
  local from="$1"
  local to="$2"
  local file="$3"
  
  if [ -f "$file" ]; then
    # 使用更精确的匹配模式，避免破坏 import 语句
    # 只替换 >Text< 形式的文本
    sed -i "s/>${from}</>${to}</g" "$file" 2>/dev/null || true
    # 替换 aria-label="Text"
    sed -i "s/aria-label=\"${from}\"/aria-label=\"${to}\"/g" "$file" 2>/dev/null || true
    # 替换 placeholder="Text"
    sed -i "s/placeholder=\"${from}\"/placeholder=\"${to}\"/g" "$file" 2>/dev/null || true
    # 替换 title="Text"
    sed -i "s/title=\"${from}\"/title=\"${to}\"/g" "$file" 2>/dev/null || true
    echo "  ✓ $file: $from -> $to"
  fi
}

# 处理每个文件
for file in "${FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "处理：$file"
    
    # 通用文本替换
    replace_text "Sign in" "登录" "$file"
    replace_text "Sign out" "退出" "$file"
    replace_text "New task" "新任务" "$file"
    replace_text "Edit task" "编辑任务" "$file"
    replace_text "Delete task" "删除任务" "$file"
    replace_text "Task title" "任务标题" "$file"
    replace_text "Task details" "任务详情" "$file"
    replace_text "Title" "标题" "$file"
    replace_text "Optional details" "可选详情" "$file"
    replace_text "Select status" "选择状态" "$file"
    replace_text "Select priority" "选择优先级" "$file"
    replace_text "Unassigned" "未分配" "$file"
    replace_text "Add tag" "添加标签" "$file"
    replace_text "Remove tag" "移除标签" "$file"
    replace_text "Add dependency" "添加依赖" "$file"
    replace_text "Remove dependency" "移除依赖" "$file"
    replace_text "Tags" "标签" "$file"
    replace_text "Priority" "优先级" "$file"
    replace_text "Status" "状态" "$file"
    replace_text "Approvals" "审批" "$file"
    replace_text "Board chat" "Board 聊天" "$file"
    replace_text "Live feed" "实时动态" "$file"
    replace_text "Board settings" "Board 设置" "$file"
    replace_text "Settings" "设置" "$file"
    replace_text "Dashboard" "仪表盘" "$file"
    replace_text "Approve" "批准" "$file"
    replace_text "Reject" "拒绝" "$file"
    replace_text "Cancel" "取消" "$file"
    replace_text "Save" "保存" "$file"
    replace_text "Delete" "删除" "$file"
    replace_text "Edit" "编辑" "$file"
    replace_text "Create" "创建" "$file"
    replace_text "Update" "更新" "$file"
    replace_text "Loading..." "加载中..." "$file"
    replace_text "Error" "错误" "$file"
    replace_text "Success" "成功" "$file"
    replace_text "Confirm" "确认" "$file"
    replace_text "Back" "返回" "$file"
    replace_text "Close" "关闭" "$file"
    replace_text "Open" "打开" "$file"
    replace_text "View" "查看" "$file"
    replace_text "Search" "搜索" "$file"
    replace_text "Filter" "筛选" "$file"
    replace_text "Refresh" "刷新" "$file"
    replace_text "Retry" "重试" "$file"
    replace_text "All" "全部" "$file"
    replace_text "None" "无" "$file"
    replace_text "Yes" "是" "$file"
    replace_text "No" "否" "$file"
    replace_text "OK" "确定" "$file"
    replace_text "Inbox" "收件箱" "$file"
    replace_text "In Progress" "进行中" "$file"
    replace_text "In Review" "审核中" "$file"
    replace_text "Completed" "已完成" "$file"
    replace_text "High" "高" "$file"
    replace_text "Medium" "中" "$file"
    replace_text "Low" "低" "$file"
    replace_text "Active" "活跃" "$file"
    replace_text "Online" "在线" "$file"
    replace_text "Offline" "离线" "$file"
  fi
done

echo ""
echo "✅ 汉化替换完成!"
echo "📦 下一步：cd /opt/openclaw-mission-control && docker compose build frontend && docker compose up -d frontend"
