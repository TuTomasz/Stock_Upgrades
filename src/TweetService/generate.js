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
      headless: false,
      slowMo: 10,
      executablePath: process.env.CHROME_PATH,
      defaultViewport: null,
    };
  
    puppeteer.launch(chromeOptions).then(async (browser) => {

    // directory to index.html file
     const page = await browser.newPage();
    await page.goto("http://127.0.0.1:8080");
  
      
     });
  })();
  
   



