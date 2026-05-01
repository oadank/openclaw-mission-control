import { useTranslations } from "next-intl";

export default function Loading() {
  const t = useTranslations("common");
  
  return (
    <div
      data-cy="route-loader"
      className="flex min-h-screen items-center justify-center bg-app px-6"
    >
      <div className="flex flex-col items-center gap-3">
        <div className="h-10 w-10 animate-spin rounded-full border-2 border-slate-200 border-t-[var(--accent)]" />
        <p className="text-sm text-slate-500">{t("loadingApp")}</p>
      </div>
    </div>
  );
}
