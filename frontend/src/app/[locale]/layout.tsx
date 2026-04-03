import type { ReactNode } from "react";

export default async function LocaleLayout({ children }: { children: ReactNode }) {
  return <div className="min-h-screen bg-app">{children}</div>;
}
