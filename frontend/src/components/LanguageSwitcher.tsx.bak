'use client';

import { useLocale } from 'next-intl';
import { usePathname, useRouter } from '@/i18n/request';

export default function LanguageSwitcher() {
  const locale = useLocale();
  const pathname = usePathname();
  const router = useRouter();

  const handleLocaleChange = (newLocale: string) => {
    router.push(pathname, { locale: newLocale });
  };

  return (
    <div className="flex items-center gap-2">
      <span className="text-sm text-gray-600">语言 / Language:</span>
      <button
        onClick={() => handleLocaleChange('zh-CN')}
        className={`px-3 py-1 text-sm rounded ${
          locale === 'zh-CN'
            ? 'bg-blue-500 text-white'
            : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
        }`}
      >
        中文
      </button>
      <button
        onClick={() => handleLocaleChange('en')}
        className={`px-3 py-1 text-sm rounded ${
          locale === 'en'
            ? 'bg-blue-500 text-white'
            : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
        }`}
      >
        English
      </button>
    </div>
  );
}
