/////////////////////////////////////////////////////////////////
///           Generate script for crating posts in PNG
/////////////////////////////////////////////////////////////////

const puppeteer = require("puppeteer-extra");
const AdblockerPlugin = require("puppeteer-extra-plugin-adblocker");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");

// Setup
puppeteer.use(StealthPlugin());
puppeteer.use(AdblockerPlugin({ blockTrackers: true }));
require("dotenv").config();
const fs = require("fs");

// Main
(async () => {
  chromeOptions = {
    headless: true,
    slowMo: 140,
    executablePath: process.env.CHROME_PATH,
    viewport: {
      width: 1920,
      height: 1080,
    },
    
  };

  puppeteer.launch(chromeOptions).then(async (browser) => {
    const page = await browser.newPage();
    
    await page.goto("http://127.0.0.1:8080");

    await page.waitForSelector(".Container");

    const elHandleArray = await page.$$(".Tweet");

    for (let el of elHandleArray) {
      const id = await el.evaluate((el) => el.id);

      await el.screenshot({ path: `./Tweets/${id}.png` });
    }
    await browser.close();
  });
})();
