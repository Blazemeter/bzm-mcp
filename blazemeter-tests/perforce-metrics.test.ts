import { test, expect } from './performance-fixture';

test('Benchmark Perforce Multi-Page User Journey', async ({ page, performanceTracker }, testInfo) => {
  // Block analytical calls to isolate pure runtime traffic
  await page.route('**/*{analytics,hubspot,doubleclick,google-analytics,linkedin}*', route => route.abort());

  // --- PAGE 1: Landing on Main Perforce site ---
  performanceTracker.resetCounters();
  await performanceTracker.startMetricsCollection(page); // Always initialize collection before navigation!
  await page.goto('https://perforce.com');
  
  try {
    await page.getByRole('button', { name: 'Accept All' }).click();
  } catch (e) {}
  
  let metrics = await performanceTracker.stop(testInfo, 'Main Landing Page');
  expect.soft(metrics.totalPageSizeMB).toBeLessThan(15.0);

  // --- PAGE 2: Browse Products ---
  performanceTracker.resetCounters();
  await performanceTracker.startMetricsCollection(page);
  await page.getByRole('link', { name: 'Browse Products' }).click();
  await page.waitForLoadState('load');
  
  metrics = await performanceTracker.stop(testInfo, 'Browse Products');

  // --- PAGE 3: Digital IP Management ---
  performanceTracker.resetCounters();
  await performanceTracker.startMetricsCollection(page);
  await page.getByRole('link', { name: 'Digital IP Management and' }).click();
  await page.waitForLoadState('load');
  
  metrics = await performanceTracker.stop(testInfo, 'Digital IP Management');

  // --- PAGE 4: Explore IPLM ---
  performanceTracker.resetCounters();
  await performanceTracker.startMetricsCollection(page);
  await page.getByRole('link', { name: 'Explore IPLM' }).click();
  await page.waitForLoadState('load');
  
  metrics = await performanceTracker.stop(testInfo, 'Explore IPLM');

  // --- PAGE 5: What’s New ---
  performanceTracker.resetCounters();
  await performanceTracker.startMetricsCollection(page);
  await page.getByRole('link', { name: 'What’s New' }).click();
  await page.waitForLoadState('load');
  
  metrics = await performanceTracker.stop(testInfo, 'What’s New');

  // --- PAGE 6: Handle Popup Redirection ---
  performanceTracker.resetCounters();
  const page1Promise = page.waitForEvent('popup');
  await page.getByRole('link', { name: 'Perforce Software' }).click();
  const page1 = await page1Promise;

  await page1.bringToFront();
  
  // Initialize metric collectors on the brand new popup page reference context
  await performanceTracker.startMetricsCollection(page1);
  
  const popupUrl = page1.url();
  await page1.goto(popupUrl);
  await page1.waitForLoadState('load');

  // Interaction triggers the Interaction to Next Paint (INP) evaluation timeline
  await page1.mouse.wheel(0, 500);
  await page1.waitForTimeout(2500); 
  
  metrics = await performanceTracker.stop(testInfo, 'Perforce Software Popup Tab', page1);
  console.log('Final Popup Metrics Summary:', JSON.stringify(metrics, null, 2));
});