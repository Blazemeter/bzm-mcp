import { test, expect } from '@playwright/test';

// Automatically inject performance tracking script into every page and popup before it loads
test.beforeEach(async ({ context }) => {
  await context.addInitScript(() => {
    // Initialize standard tracking metrics container
    window['__webVitals'] = { lcp: 0, cls: 0, ttfb: 0 };

    // 1. Capture Time To First Byte (TTFB)
    const [navEntry] = performance.getEntriesByType('navigation');
    if (navEntry) {
      window['__webVitals'].ttfb = navEntry.responseStart - navEntry.requestStart;
    }

    // 2. Continuous Observer for LCP and CLS
    const observer = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (entry.entryType === 'largest-contentful-paint') {
          window['__webVitals'].lcp = entry.startTime;
        }
        if (entry.entryType === 'layout-shift' && !entry.hadRecentInput) {
          window['__webVitals'].cls += entry.value;
        }
      }
    });

    observer.observe({ type: 'largest-contentful-paint', buffered: true });
    observer.observe({ type: 'layout-shift', buffered: true });
  });
});

// Helper function to safely fetch, format, and log the metrics
async function logWebVitals(page, pageLabel: string) {
  // Brief timeout allows any layout shifts or LCP calculations during rendering to register
  await page.waitForTimeout(500); 
  
  const vitals = await page.evaluate(() => window['__webVitals']);
  
  console.log(`\n========================================`);
  console.log(`📊 Web Vitals for [${pageLabel}]`);
  console.log(`----------------------------------------`);
  console.log(`⏱️  TTFB (Time to First Byte): ${vitals?.ttfb ? vitals.ttfb.toFixed(2) + 'ms' : 'N/A'}`);
  console.log(`🖼️  LCP (Largest Contentful Paint): ${vitals?.lcp ? vitals.lcp.toFixed(2) + 'ms' : 'N/A'}`);
  console.log(`🧱  CLS (Cumulative Layout Shift): ${vitals?.cls ? vitals.cls.toFixed(4) : '0.0000'}`);
  console.log(`========================================`);
}

test('test', async ({ page }) => {
  // Page 1: Landing on Main Perforce site
  await page.goto('https://perforce.com');
  await page.getByRole('button', { name: 'Accept All' }).click();
  await logWebVitals(page, 'Main Landing Page');

  // Page 2: Browse Products
  await page.getByRole('link', { name: 'Browse Products' }).click();
  await page.waitForLoadState('domcontentloaded');
  await logWebVitals(page, 'Browse Products');

  // Page 3: Digital IP Management
  await page.getByRole('link', { name: 'Digital IP Management and' }).click();
  await page.waitForLoadState('domcontentloaded');
  await logWebVitals(page, 'Digital IP Management');

  // Page 4: Explore IPLM
  await page.getByRole('link', { name: 'Explore IPLM' }).click();
  await page.waitForLoadState('domcontentloaded');
  await logWebVitals(page, 'Explore IPLM');

  // Page 5: What’s New
  await page.getByRole('link', { name: 'What’s New' }).click();
  await page.waitForLoadState('domcontentloaded');
  await logWebVitals(page, 'What’s New');

  // Page 6: Handle Popup redirection
  const page1Promise = page.waitForEvent('popup');
  await page.getByRole('link', { name: 'Perforce Software' }).click();
  const page1 = await page1Promise;
  
  // Wait for the popup page to finalize loading before fetching data
  await page1.waitForLoadState('domcontentloaded');
  await logWebVitals(page1, 'Perforce Software Popup Tab');
});

