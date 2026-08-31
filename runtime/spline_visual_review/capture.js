const { chromium } = require('../../spline/node_modules/@playwright/test');

const competitors = [
  ['competitor-sh-mobile.png', 'https://shamsiiii19.github.io/sh/'],
  ['competitor-lll-mobile.png', 'https://albinagas.github.io/lll/'],
  ['competitor-smm-mobile.png', 'https://samirka11.github.io/smm/'],
  ['competitor-samirprobrand-mobile.png', 'https://nissanr34ol.github.io/samirprobrand/'],
];

async function settle(page) {
  await page.locator('body').waitFor({ timeout: 15000 });
  await page.evaluate(() => document.fonts && document.fonts.ready);
  await page.waitForTimeout(1400);
}

(async () => {
  const url = process.env.SPLINE_URL;
  if (!url) throw new Error('SPLINE_URL missing');
  const browser = await chromium.launch({ headless: true });

  const mobile = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
  await mobile.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await mobile.locator('main').waitFor({ timeout: 15000 });
  await settle(mobile);
  await mobile.screenshot({ path: 'spline-mobile-full.png', fullPage: true });
  await mobile.locator('.hero').screenshot({ path: 'spline-mobile-hero.png' });
  await mobile.locator('.requestSection').screenshot({ path: 'spline-mobile-form.png' });
  await mobile.close();

  const desktop = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
  await desktop.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await desktop.locator('main').waitFor({ timeout: 15000 });
  await settle(desktop);
  await desktop.screenshot({ path: 'spline-desktop-full.png', fullPage: true });
  await desktop.close();

  for (const [path, competitorUrl] of competitors) {
    const page = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
    await page.goto(competitorUrl, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await settle(page);
    await page.screenshot({ path, fullPage: false });
    await page.close();
    console.log(`COMPETITOR_RENDER_CAPTURED ${competitorUrl}`);
  }

  await browser.close();
  console.log('SPLINE_AND_COMPETITOR_RENDERS_CAPTURED');
})().catch((error) => {
  console.error(error);
  process.exit(1);
});
