const { chromium } = require('../../spline/node_modules/@playwright/test');

(async () => {
  const url = process.env.SPLINE_URL;
  if (!url) throw new Error('SPLINE_URL missing');
  const browser = await chromium.launch({ headless: true });

  const mobile = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
  await mobile.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await mobile.locator('main').waitFor({ timeout: 15000 });
  await mobile.evaluate(() => document.fonts.ready);
  await mobile.waitForTimeout(1200);
  await mobile.screenshot({ path: 'mobile-full.png', fullPage: true });
  await mobile.locator('.process').screenshot({ path: 'mobile-process.png' });
  await mobile.close();

  const desktop = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
  await desktop.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await desktop.locator('main').waitFor({ timeout: 15000 });
  await desktop.evaluate(() => document.fonts.ready);
  await desktop.waitForTimeout(1200);
  await desktop.screenshot({ path: 'desktop-full.png', fullPage: true });
  await desktop.close();

  await browser.close();
  console.log('SPLINE_RENDER_CAPTURED');
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
