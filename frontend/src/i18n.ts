export const locales = ['en', 'zh-CN'] as const;
export type Locale = (typeof locales)[number];

export const defaultLocale: Locale = 'zh-CN';

export function isLocale(locale: string): locale is Locale {
  return locales.includes(locale as Locale);
}
