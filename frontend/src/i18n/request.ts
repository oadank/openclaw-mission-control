import { getRequestConfig } from 'next-intl/server';
import { defaultLocale, isLocale } from '@/i18n';

export default getRequestConfig(async ({ requestLocale }) => {
  const locale = await requestLocale;
  const validLocale = locale && isLocale(locale) ? locale : defaultLocale;
  
  return {
    locale: validLocale,
    messages: (await import(`../../messages/${validLocale}.json`)).default,
  };
});
