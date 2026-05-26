import { test, expect } from './performance-fixture';
import { Page } from '@playwright/test';

test.describe.serial('Perforce Multi-Page Benchmarks', () => {
  let sharedPage: Page;

  test.beforeAll(async ({ browser }) => {
    const context = await browser.newContext();
    sharedPage = await context.newPage();
    await sharedPage.route('**/*{analytics,hubspot,doubleclick,google-analytics,linkedin}*', route => route.abort());
  });

  test.afterAll(async () => {
    await sharedPage.close();
  });

  test('Step 1: Main Landing Page', async ({ performanceTracker }, testInfo) => {
    performanceTracker.resetCounters();
    // 1. Start collecting FIRST
    await performanceTracker.startMetricsCollection(sharedPage); 
    // 2. Perform action
    await sharedPage.goto('https://perforce.com');
    
    try {
      await sharedPage.getByRole('button', { name: 'Accept All' }).click();
    } catch (e) {}
    
    const metrics = await performanceTracker.stop(testInfo, 'Main Landing Page', sharedPage);
    expect.soft(metrics.totalPageSizeMB).toBeLessThan(15.0);
  });

  test('Step 2: Browse Products', async ({ performanceTracker }, testInfo) => {
    performanceTracker.resetCounters();
    // 1. Start collecting FIRST so we don't miss the click traffic!
    await performanceTracker.startMetricsCollection(sharedPage);
    
    // 2. Perform action
    await sharedPage.getByRole('link', { name: 'Browse Products' }).click();
    await sharedPage.waitForLoadState('load');
    
    await performanceTracker.stop(testInfo, 'Browse Products', sharedPage);
  });

  test('Step 3: Digital IP Management', async ({ performanceTracker }, testInfo) => {
    performanceTracker.resetCounters();
    await performanceTracker.startMetricsCollection(sharedPage);
    
    await sharedPage.getByRole('link', { name: 'Digital IP Management and' }).click();
    await sharedPage.waitForLoadState('load');
    
    await performanceTracker.stop(testInfo, 'Digital IP Management', sharedPage);
  });

  test('Step 4: Explore IPLM', async ({ performanceTracker }, testInfo) => {
    performanceTracker.resetCounters();
    await performanceTracker.startMetricsCollection(sharedPage);
    
    await sharedPage.getByRole('link', { name: 'Explore IPLM' }).click();
    await sharedPage.waitForLoadState('load');
    
    await performanceTracker.stop(testInfo, 'Explore IPLM', sharedPage);
  });

  test('Step 5: What’s New', async ({ performanceTracker }, testInfo) => {
    performanceTracker.resetCounters();
    await performanceTracker.startMetricsCollection(sharedPage);
    
    await sharedPage.getByRole('link', { name: 'What’s New' }).click();
    await sharedPage.waitForLoadState('load');
    
    await performanceTracker.stop(testInfo, 'What’s New', sharedPage);
  });

  test('Step 6: Perforce Software Popup Tab', async ({ performanceTracker }, testInfo) => {
    performanceTracker.resetCounters();
    const page1Promise = sharedPage.waitForEvent('popup');
    await sharedPage.getByRole('link', { name: 'Perforce Software' }).click();
    const page1 = await page1Promise;

    await page1.bringToFront();
    await performanceTracker.startMetricsCollection(page1);
    
    const popupUrl = page1.url();
    await page1.goto(popupUrl);
    await page1.waitForLoadState('load');

    await page1.mouse.wheel(0, 500);
    await page1.waitForTimeout(2500); 
    
    const metrics = await performanceTracker.stop(testInfo, 'Perforce Software Popup Tab', page1);
    console.log('Final Popup Metrics Summary:', JSON.stringify(metrics, null, 2));
  });
});
