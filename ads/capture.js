const { chromium } = require('playwright');
const path = require('path');

async function captureCards(page, file, prefix, count) {
  await page.goto(`file://${path.resolve(__dirname, file)}`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2500);
  for (let i = 1; i <= count; i++) {
    const sel = `#${prefix}${i}`;
    const el = await page.locator(sel);
    const out = `output/${prefix.replace(/[^a-z0-9]/gi, '-')}${i}.png`;
    await el.screenshot({ path: path.resolve(__dirname, out), type: 'png' });
    console.log(`✓ ${out}`);
  }
}

async function captureById(page, file, ids) {
  await page.goto(`file://${path.resolve(__dirname, file)}`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2500);
  for (const id of ids) {
    const el = await page.locator(`#${id}`);
    await el.screenshot({ path: path.resolve(__dirname, `output/${id}.png`), type: 'png' });
    console.log(`✓ ${id}.png`);
  }
}

async function capture() {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  // Carousel 1: Safety
  await captureCards(page, 'carousel-safety.html', 'card', 5);

  // Carousel 2: NEET/Student Focus
  await captureCards(page, 'carousel-jee-focus.html', 'jee', 5);

  // Carousel 3: Parent Fear
  await captureCards(page, 'carousel-parent-fear.html', 'pf', 5);

  // Carousel 4: Durgapur Rush (urgency)
  await captureCards(page, 'carousel-durgapur-rush.html', 'dr', 5);

  // Carousel 5: FOMO / Vacancy (urgency)
  await captureCards(page, 'carousel-fomo-vacancy.html', 'fomo', 5);

  // Meme backgrounds
  await captureById(page, 'meme-backgrounds.html', [
    'meme-exam-panic', 'meme-reality-check', 'meme-parent-dialogue', 'meme-sisterhood'
  ]);

  // Static ads (original)
  await captureById(page, 'static-ads.html', ['static-square', 'static-vertical']);

  // Static ads (extra)
  await captureById(page, 'statics-extra.html', [
    'curiosity-square', 'specificity-square', 'emotional-vertical', 'urgency-square'
  ]);

  await browser.close();
  console.log('\n✅ All creatives captured → ads/output/');
}

capture().catch(console.error);
