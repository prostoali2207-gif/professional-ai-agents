const { chromium } = require('../../spline/node_modules/@playwright/test');

(async () => {
  const url = process.env.SPLINE_PREVIEW_URL;
  if (!url) throw new Error('SPLINE_PREVIEW_URL missing');
  const browser = await chromium.launch({ headless: true });

  for (const [name, width, height] of [
    ['mobile-390', 390, 844],
    ['intermediate-768', 768, 960],
    ['desktop-1440', 1440, 1000],
  ]) {
    const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.locator('main').waitFor({ timeout: 15000 });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(1000);
    await page.screenshot({ path: `${name}-full.png`, fullPage: true });
    if (width === 390) {
      await page.locator('.process').screenshot({ path: 'mobile-390-process.png' });
    }
    await page.close();
  }

  await browser.close();
  console.log('UI_GUARD_RENDER_CAPTURED');
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
