const puppeteer = require("puppeteer-extra");

// Add stealth plugin and use defaults (all tricks to hide puppeteer usage)
const StealthPlugin = require("puppeteer-extra-plugin-stealth");
puppeteer.use(StealthPlugin());

// Add adblocker plugin to block all ads and trackers (saves bandwidth)
const AdblockerPlugin = require("puppeteer-extra-plugin-adblocker");
puppeteer.use(AdblockerPlugin({ blockTrackers: true }));

// import env variables
require("dotenv").config();

//import file system
const fs = require("fs");

// self invoking main function
(async () => {
  chromeOptions = {
    headless: true,
    slowMo: 140,
    executablePath: process.env.CHROME_PATH,
     viewport:{
      width: 1920,
      height: 1080,
    }
  };

  puppeteer.launch(chromeOptions).then(async (browser) => {
    // directory to index.html file
    const page = await browser.newPage();
    await page.goto("http://127.0.0.1:8080");

    // wait forh page to load
    await page.waitForSelector(".Container");

    const elHandleArray = await page.$$(".Tweet");
    for (let el of elHandleArray) {
      const id = await el.evaluate((el) => el.id);
      const analists = await el.evaluate((el) => el.id);
   
      await page.waitFor(Math.random() * (3000 - 1000) + 1000);

      el.screenshot({ path: `./Tweets/${id}.png` });
    }
    

    await browser.close();
  });
})();
