const { chromium } = require('../../spline/node_modules/@playwright/test');

async function settle(page) {
  await page.locator('body').waitFor({ timeout: 15000 });
  await page.evaluate(() => document.fonts && document.fonts.ready);
  await page.waitForTimeout(1000);
}

async function capture(browser, width, height, name) {
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
  await page.goto(process.env.SPLINE_URL, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.locator('main').waitFor({ timeout: 15000 });
  await settle(page);
  await page.screenshot({ path: `${name}-full.png`, fullPage: true });
  await page.locator('.hero').screenshot({ path: `${name}-hero.png` });
  await page.locator('.process').screenshot({ path: `${name}-process.png` });
  await page.locator('.requestSection').screenshot({ path: `${name}-request.png` });
  const overflow = await page.evaluate(() => ({
    viewport: document.documentElement.clientWidth,
    bodyScroll: document.body.scrollWidth,
    docScroll: document.documentElement.scrollWidth,
  }));
  require('fs').writeFileSync(`${name}-layout.json`, JSON.stringify(overflow, null, 2));
  await page.close();
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  await capture(browser, 390, 844, 'ui-guard-390');
  await capture(browser, 768, 1024, 'ui-guard-768');
  await capture(browser, 1440, 1000, 'ui-guard-1440');
  await browser.close();
  console.log('UI_GUARD_RENDERS_CAPTURED');
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
