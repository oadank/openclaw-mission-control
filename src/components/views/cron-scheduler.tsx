"use client";

import { useState, useEffect, useCallback } from "react";
import {
  Clock,
  Plus,
  Play,
  Pause,
  RotateCcw,
  Trash2,
  Loader2,
  Calendar,
  Bot,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface ScheduleObject {
  kind?: string;
  everyMs?: number;
  cron?: string;
  anchorMs?: number;
}

interface CronJob {
  id: string;
  prompt?: string;
  schedule: string | ScheduleObject;
  enabled: boolean;
  agentId?: string;
  lastRun?: string;
  nextRun?: string;
}

// Human-friendly schedule presets
const SCHEDULE_PRESETS = [
  { label: "每小时", cron: "0 * * * *" },
  { label: "每天 09:00", cron: "0 9 * * *" },
  { label: "每天 18:00", cron: "0 18 * * *" },
  { label: "工作日 09:00", cron: "0 9 * * 1-5" },
  { label: "每周一 09:00", cron: "0 9 * * 1" },
  { label: "每周日 02:00", cron: "0 2 * * 0" },
  { label: "每15分钟", cron: "*/15 * * * *" },
  { label: "每30分钟", cron: "*/30 * * * *" },
  { label: "每天两次（9点/18点）", cron: "0 9,18 * * *" },
  { label: "每月1日", cron: "0 9 1 * *" },
];

function formatMs(ms: number): string {
  if (ms < 60_000) return `${Math.round(ms / 1000)} seconds`;
  if (ms < 3_600_000) return `${Math.round(ms / 60_000)} minutes`;
  if (ms < 86_400_000) return `${Math.round(ms / 3_600_000)} hours`;
  return `${Math.round(ms / 86_400_000)} days`;
}

function scheduleToHuman(schedule: string | ScheduleObject): string {
  if (typeof schedule === "object" && schedule !== null) {
    if (schedule.kind === "every" && schedule.everyMs) {
      return `Every ${formatMs(schedule.everyMs)}`;
    }
    if (schedule.kind === "cron" && schedule.cron) {
      return cronToHuman(schedule.cron);
    }
    if (schedule.everyMs) {
      return `Every ${formatMs(schedule.everyMs)}`;
    }
    return "自定义计划";
  }
  if (typeof schedule !== "string") return "自定义计划";
  return cronToHuman(schedule);
}

function cronToHuman(cron: string): string {
  const preset = SCHEDULE_PRESETS.find((p) => p.cron === cron);
  if (preset) return preset.label;

  const parts = cron.split(" ");
  if (parts.length !== 5) return cron;

  const [min, hour, dom, , dow] = parts;

  if (min === "0" && hour !== "*" && dom === "*" && dow === "*") {
    const h = parseInt(hour);
    const ampm = h >= 12 ? "PM" : "AM";
    const h12 = h === 0 ? 12 : h > 12 ? h - 12 : h;
    return `Every day at ${h12}:00 ${ampm}`;
  }
  if (min.startsWith("*/")) return `Every ${min.slice(2)} minutes`;
  if (hour.startsWith("*/")) return `Every ${hour.slice(2)} hours`;
  return cron;
}

function timeAgo(dateStr: string | undefined): string {
  if (!dateStr) return "Never";
  const date = new Date(dateStr);
  if (isNaN(date.getTime())) return dateStr;
  const seconds = Math.floor((Date.now() - date.getTime()) / 1000);
  if (seconds < 0) {
    const future = Math.abs(seconds);
    if (future < 3600) return `in ${Math.floor(future / 60)}m`;
    if (future < 86400) return `in ${Math.floor(future / 3600)}h`;
    return `in ${Math.floor(future / 86400)}d`;
  }
  if (seconds < 60) return "刚刚";
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
  return `${Math.floor(seconds / 86400)}d ago`;
}

export function CronScheduler() {
  const [jobs, setJobs] = useState<CronJob[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<string | null>(null);
  const [showCreate, setShowCreate] = useState(false);
  const [expandedJob, setExpandedJob] = useState<string | null>(null);

  // Create form state
  const [newPrompt, setNewPrompt] = useState("");
  const [newSchedule, setNewSchedule] = useState(SCHEDULE_PRESETS[1].cron);
  const [newAgent, setNewAgent] = useState("main");
  const [creating, setCreating] = useState(false);

  const fetchJobs = useCallback(async () => {
    try {
      const res = await fetch("/api/openclaw/cron");
      const data = await res.json();
      setJobs(Array.isArray(data.jobs) ? data.jobs : []);
    } catch {
      setJobs([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchJobs();
    const interval = setInterval(fetchJobs, 10000);
    return () => clearInterval(interval);
  }, [fetchJobs]);

  const createJob = async () => {
    if (!newPrompt.trim()) return;
    setCreating(true);
    try {
      await fetch("/api/openclaw/cron", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action: "add",
          prompt: newPrompt,
          schedule: newSchedule,
          agentId: newAgent,
          enabled: true,
        }),
      });
      setNewPrompt("");
      setShowCreate(false);
      await fetchJobs();
    } finally {
      setCreating(false);
    }
  };

  const toggleJob = async (id: string, enabled: boolean) => {
    setActionLoading(id);
    try {
      await fetch("/api/openclaw/cron", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "update", id, enabled: !enabled }),
      });
      await fetchJobs();
    } finally {
      setActionLoading(null);
    }
  };

  const runNow = async (id: string) => {
    setActionLoading(id);
    try {
      await fetch("/api/openclaw/cron", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "run", id, mode: "force" }),
      });
      await fetchJobs();
    } finally {
      setActionLoading(null);
    }
  };

  const removeJob = async (id: string) => {
    setActionLoading(id);
    try {
      await fetch("/api/openclaw/cron", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action: "remove", id }),
      });
      await fetchJobs();
    } finally {
      setActionLoading(null);
    }
  };

  return (
    <div className="flex-1 overflow-hidden flex flex-col">
      {/* Header */}
      <div className="p-6 border-b border-border bg-card/30">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded bg-primary/10 flex items-center justify-center">
              <Calendar className="w-5 h-5 text-primary" />
            </div>
            <div>
              <h2 className="text-xl font-bold">定时任务</h2>
              <p className="text-sm text-muted-foreground">
                设置周期性 AI 任务（按计划自动执行）
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <Badge variant="secondary" className="font-mono">
              {jobs.filter((j) => j.enabled).length} 活跃
            </Badge>
            <Button onClick={() => setShowCreate(true)} className="gap-1.5">
              <Plus className="w-4 h-4" />
              新建任务
            </Button>
          </div>
        </div>
      </div>

      <ScrollArea className="flex-1 p-6">
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="w-6 h-6 animate-spin text-primary" />
          </div>
        ) : jobs.length === 0 ? (
          <div className="text-center py-16">
            <Clock className="w-14 h-14 mx-auto mb-3 text-muted-foreground opacity-30" />
            <p className="text-lg font-medium mb-1">暂无定时任务</p>
            <p className="text-sm text-muted-foreground mb-4">
              创建你的第一个周期任务
            </p>
            <Button onClick={() => setShowCreate(true)} className="gap-1.5">
              <Plus className="w-4 h-4" />
              创建任务
            </Button>
          </div>
        ) : (
          <div className="space-y-3">
            {jobs.map((job) => {
              const isExpanded = expandedJob === job.id;
              const isLoading = actionLoading === job.id;
              return (
                <div
                  key={job.id}
                  className={`glass-panel rounded-lg overflow-hidden transition-all ${
                    job.enabled
                      ? "border-l-4 border-l-green-500/50"
                      : "border-l-4 border-l-muted/50 opacity-70"
                  }`}
                >
                  <div className="p-4 flex items-center gap-4">
                    {/* Status indicator */}
                    <div
                      className={`w-2.5 h-2.5 rounded-full shrink-0 ${
                        job.enabled ? "bg-green-500" : "bg-muted-foreground"
                      }`}
                    />

                    {/* Info */}
                    <div className="flex-1 min-w-0">
                      <div className="font-medium text-sm truncate">
                        {job.prompt || "未命名任务"}
                      </div>
                      <div className="flex items-center gap-3 mt-1 text-xs text-muted-foreground">
                        <span className="flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          {scheduleToHuman(job.schedule)}
                        </span>
                        <span className="flex items-center gap-1">
                          <Bot className="w-3 h-3" />
                          {job.agentId || "main"}
                        </span>
                        {job.nextRun && (
                          <span>Next: {timeAgo(job.nextRun)}</span>
                        )}
                      </div>
                    </div>

                    {/* Actions */}
                    <div className="flex items-center gap-1.5 shrink-0">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => runNow(job.id)}
                        disabled={isLoading}
                        className="gap-1 text-xs h-8"
                        title="立即执行"
                      >
                        {isLoading ? (
                          <Loader2 className="w-3.5 h-3.5 animate-spin" />
                        ) : (
                          <Play className="w-3.5 h-3.5" />
                        )}
                        Run
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => toggleJob(job.id, job.enabled)}
                        disabled={isLoading}
                        className="gap-1 text-xs h-8"
                        title={job.enabled ? "暂停" : "恢复"}
                      >
                        {job.enabled ? (
                          <Pause className="w-3.5 h-3.5" />
                        ) : (
                          <RotateCcw className="w-3.5 h-3.5" />
                        )}
                        {job.enabled ? "暂停" : "恢复"}
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() =>
                          setExpandedJob(isExpanded ? null : job.id)
                        }
                        className="h-8 w-8 p-0"
                      >
                        {isExpanded ? (
                          <ChevronUp className="w-4 h-4" />
                        ) : (
                          <ChevronDown className="w-4 h-4" />
                        )}
                      </Button>
                    </div>
                  </div>

                  {/* Expanded details */}
                  {isExpanded && (
                    <div className="px-4 pb-4 pt-0 border-t border-border ml-6">
                      <div className="grid grid-cols-2 gap-3 py-3 text-xs">
                        <div>
                          <span className="text-muted-foreground">计划：</span>{" "}
                          <span className="font-mono">{scheduleToHuman(job.schedule)}</span>
                        </div>
                        <div>
                          <span className="text-muted-foreground">代理：</span>{" "}
                          {job.agentId || "main"}
                        </div>
                        <div>
                          <span className="text-muted-foreground">上次执行：</span>{" "}
                          {timeAgo(job.lastRun)}
                        </div>
                        <div>
                          <span className="text-muted-foreground">下次执行：</span>{" "}
                          {timeAgo(job.nextRun)}
                        </div>
                      </div>
                      <div className="flex gap-2 pt-2">
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => removeJob(job.id)}
                          disabled={isLoading}
                          className="gap-1 text-xs text-red-400 border-red-400/20 hover:bg-red-400/10"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                          删除
                        </Button>
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </ScrollArea>

      {/* Create dialog */}
      <Dialog open={showCreate} onOpenChange={setShowCreate}>
        <DialogContent className="sm:max-w-lg">
          <DialogHeader>
            <DialogTitle>创建新定时任务</DialogTitle>
            <DialogDescription>
              告诉你的 AI 代理要做什么，以及执行频率。
            </DialogDescription>
          </DialogHeader>

          <div className="space-y-4 py-2">
            {/* Prompt */}
            <div>
              <label className="block text-sm font-medium mb-1.5">
                AI 要做什么？
              </label>
              <textarea
                value={newPrompt}
                onChange={(e) => setNewPrompt(e.target.value)}
                placeholder="总结我的未读邮件并给我一个简报"
                rows={3}
                className="w-full px-3 py-2 bg-background border border-border rounded text-sm focus:outline-none focus:ring-1 focus:ring-primary resize-none"
              />
            </div>

            {/* Schedule */}
            <div>
              <label className="block text-sm font-medium mb-1.5">
                执行频率
              </label>
              <Select value={newSchedule} onValueChange={setNewSchedule}>
                <SelectTrigger>
                  <SelectValue placeholder="选择计划" />
                </SelectTrigger>
                <SelectContent>
                  {SCHEDULE_PRESETS.map((p) => (
                    <SelectItem key={p.cron} value={p.cron}>
                      {p.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Agent */}
            <div>
              <label className="block text-sm font-medium mb-1.5">
                使用哪个代理？
              </label>
              <input
                type="text"
                value={newAgent}
                onChange={(e) => setNewAgent(e.target.value)}
                placeholder="main"
                className="w-full px-3 py-2 bg-background border border-border rounded text-sm font-mono focus:outline-none focus:ring-1 focus:ring-primary"
              />
            </div>
          </div>

          <DialogFooter>
            <Button variant="outline" onClick={() => setShowCreate(false)}>
              Cancel
            </Button>
            <Button
              onClick={createJob}
              disabled={creating || !newPrompt.trim()}
              className="gap-1.5"
            >
              {creating ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Plus className="w-4 h-4" />
              )}
              创建任务
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}


