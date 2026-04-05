#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const projectRoot = '/home/node/.openclaw/workspace/openclaw-mission-control/frontend';
const srcDir = path.join(projectRoot, 'src');

// Results storage
const results = {
  filesWithHardcodedText: [],
  filesWithUseTranslations: [],
  hardcodedTexts: [],
  missingTranslationKeys: [],
  allTextHits: []
};

// Common patterns
const useTranslationsPattern = /useTranslations\s*\(\s*['"]([^'"]+)['"]?\s*\)/g;
const tFunctionPattern = /\bt\s*\(\s*['"]([^'"]+)['"]/g;
const hardcodedTextPattern = />([A-Z][^<>]{2,})</g;

// Scan all .tsx and .ts files
function scanDirectory(dir) {
  const files = fs.readdirSync(dir);
  
  for (const file of files) {
    const fullPath = path.join(dir, file);
    const stat = fs.statSync(fullPath);
    
    if (stat.isDirectory()) {
      scanDirectory(fullPath);
    } else if (file.endsWith('.tsx') || file.endsWith('.ts')) {
      scanFile(fullPath);
    }
  }
}

function scanFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const relativePath = path.relative(projectRoot, filePath);
  
  // Check for useTranslations
  const hasUseTranslations = content.includes('useTranslations');
  if (hasUseTranslations) {
    results.filesWithUseTranslations.push(relativePath);
  }
  
  // Extract t() calls
  const tCalls = [];
  let match;
  tFunctionPattern.lastIndex = 0;
  while ((match = tFunctionPattern.exec(content)) !== null) {
    tCalls.push(match[1]);
  }
  
  // Look for hardcoded English text (simple heuristic)
  const lines = content.split('\n');
  const fileHardcoded = [];
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    // Skip comments
    if (line.trim().startsWith('//') || line.trim().startsWith('/*')) continue;
    
    // Look for English text in JSX
    // Pattern: >Some English Text<
    const jsxTextMatches = line.match(/>([A-Z][a-zA-Z\s]{3,})</g);
    if (jsxTextMatches) {
      for (const m of jsxTextMatches) {
        const text = m.slice(1, -1).trim();
        if (text && text.length > 2 && !text.includes('{') && !text.includes('}')) {
          fileHardcoded.push({
            line: i + 1,
            text: text,
            context: line.trim()
          });
        }
      }
    }
    
    // Look for placeholder, aria-label, alt, title attributes
    const attrPatterns = [
      /placeholder="([A-Z][^"]{3,})"/g,
      /aria-label="([A-Z][^"]{3,})"/g,
      /alt="([A-Z][^"]{3,})"/g,
      /title="([A-Z][^"]{3,})"/g
    ];
    
    for (const pattern of attrPatterns) {
      pattern.lastIndex = 0;
      while ((match = pattern.exec(line)) !== null) {
        fileHardcoded.push({
          line: i + 1,
          text: match[1],
          context: line.trim()
        });
      }
    }
  }
  
  if (fileHardcoded.length > 0) {
    results.filesWithHardcodedText.push({
      file: relativePath,
      hits: fileHardcoded
    });
    
    for (const hit of fileHardcoded) {
      results.allTextHits.push({
        file: relativePath,
        ...hit
      });
    }
  }
}

console.log('🔍 Scanning files...');
scanDirectory(srcDir);

// Load existing translations
let enJson = {};
let zhCnJson = {};
try {
  enJson = JSON.parse(fs.readFileSync(path.join(projectRoot, 'messages', 'en.json'), 'utf-8'));
  zhCnJson = JSON.parse(fs.readFileSync(path.join(projectRoot, 'messages', 'zh-CN.json'), 'utf-8'));
} catch (e) {
  console.log('⚠️  Could not load translation files');
}

// Generate report
const report = {
  summary: {
    totalFilesScanned: 0,
    filesWithUseTranslations: results.filesWithUseTranslations.length,
    filesWithHardcodedText: results.filesWithHardcodedText.length,
    totalHardcodedHits: results.allTextHits.length,
    existingEnKeys: Object.keys(flattenObject(enJson)).length,
    existingZhKeys: Object.keys(flattenObject(zhCnJson)).length
  },
  filesByPriority: {
    critical: [],
    high: [],
    medium: [],
    low: []
  },
  allHardcodedTexts: results.allTextHits,
  filesList: {
    withUseTranslations: results.filesWithUseTranslations,
    withHardcodedText: results.filesWithHardcodedText.map(f => f.file)
  }
};

// Categorize files by priority
for (const fileResult of results.filesWithHardcodedText) {
  const filePath = fileResult.file;
  const hitCount = fileResult.hits.length;
  
  let priority = 'low';
  if (filePath.includes('page.tsx') || filePath.includes('layout.tsx')) {
    priority = hitCount > 10 ? 'critical' : 'high';
  } else if (filePath.includes('components/')) {
    priority = hitCount > 5 ? 'high' : 'medium';
  } else if (hitCount > 20) {
    priority = 'critical';
  } else if (hitCount > 10) {
    priority = 'high';
  } else if (hitCount > 5) {
    priority = 'medium';
  }
  
  report.filesByPriority[priority].push({
    file: filePath,
    hitCount: hitCount,
    hits: fileResult.hits
  });
}

// Sort by hit count descending
for (const priority of Object.keys(report.filesByPriority)) {
  report.filesByPriority[priority].sort((a, b) => b.hitCount - a.hitCount);
}

// Helper to flatten nested object
function flattenObject(obj, prefix = '') {
  const result = {};
  for (const [key, value] of Object.entries(obj)) {
    const fullKey = prefix ? `${prefix}.${key}` : key;
    if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
      Object.assign(result, flattenObject(value, fullKey));
    } else {
      result[fullKey] = value;
    }
  }
  return result;
}

// Write report
const outputPath = path.join(projectRoot, '..', 'i18n-scan-report.json');
fs.writeFileSync(outputPath, JSON.stringify(report, null, 2));

console.log(`✅ Scan complete! Report written to: ${outputPath}`);
console.log('\n📊 Summary:');
console.log(`  - Files with useTranslations: ${report.summary.filesWithUseTranslations}`);
console.log(`  - Files with hardcoded text: ${report.summary.filesWithHardcodedText}`);
console.log(`  - Total hardcoded hits: ${report.summary.totalHardcodedHits}`);
console.log(`  - Existing en.json keys: ${report.summary.existingEnKeys}`);
console.log(`  - Existing zh-CN.json keys: ${report.summary.existingZhKeys}`);

console.log('\n🎯 Priority files:');
console.log(`  Critical: ${report.filesByPriority.critical.length}`);
console.log(`  High: ${report.filesByPriority.high.length}`);
console.log(`  Medium: ${report.filesByPriority.medium.length}`);
console.log(`  Low: ${report.filesByPriority.low.length}`);
