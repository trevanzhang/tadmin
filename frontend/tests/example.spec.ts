import { test, expect } from '@playwright/test';

test('homepage has correct title', async ({ page }) => {
  await page.goto('/');

  // Expect a title "to contain" a substring.
  await expect(page).toHaveTitle(/Pure Admin Thin/);

  // Take a screenshot for debugging
  await page.screenshot({ path: 'test-screenshot.png' });
});

test('debug page load', async ({ page }) => {
  // Enable debugging
  await page.goto('/');

  // Wait for page to be fully loaded
  await page.waitForLoadState('networkidle');

  // Log page title and URL
  console.log('Page title:', await page.title());
  console.log('Current URL:', page.url());

  // Check for any console errors
  page.on('console', (message) => {
    if (message.type() === 'error') {
      console.error('Console error:', message.text());
    }
  });

  // Get page content for inspection
  const content = await page.content();
  console.log('Page HTML length:', content.length);

  // Screenshot for visual debugging
  await page.screenshot({
    path: 'debug-screenshot.png',
    fullPage: true
  });
});