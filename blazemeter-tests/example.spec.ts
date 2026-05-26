import { test, expect } from './performance-fixture';

test('Benchmark homepage performance', async ({ page, performanceTracker }, testInfo) => {
  // 1. Tell the library to start listening
  await performanceTracker.start();

  // 2. Perform your standard user flow
  await page.goto('https://example.com');
  await page.click('#hero-cta-button'); 
  await page.waitForLoadState('networkidle');

  // FIX: Capture the returned metrics from the stop method
  const metrics = await performanceTracker.stop(testInfo);

  // 4. Print or Save the results
  console.log('Test Metrics Summary:', JSON.stringify(metrics, null, 2));

  // 5. Enforce SLA / Budgets directly in your test assertion block
  expect(metrics.vitals.LCP).toBeLessThan(2500); 
  expect(metrics.network.totalPageSizeMB).toBeLessThan(3.5); 
  expect(metrics.network.requestCount).toBeLessThan(50); 
});
