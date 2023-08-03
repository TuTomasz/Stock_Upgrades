/////////////////////////////////////////////////////////////////
///           Tweet script for posting insight
/////////////////////////////////////////////////////////////////

const puppeteer = require("puppeteer-extra");
const RecaptchaPlugin = require("puppeteer-extra-plugin-recaptcha");
const AdblockerPlugin = require("puppeteer-extra-plugin-adblocker");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");

// Setup
puppeteer.use(StealthPlugin());
puppeteer.use(AdblockerPlugin({ blockTrackers: true }));
require("dotenv").config();
const fs = require("fs");

// Puppetier Setup
puppeteer.use(
  RecaptchaPlugin({
    provider: {
      id: "2captcha",
      token: process.env.CAPTCHA_KEY,
    },
    visualFeedback: true,
  })
);

// Main
(async () => {
  chromeOptions = {
    headless: true,
    slowMo: 10,
    //executablePath: process.env.CHROME_PATH,
    //defaultViewport: 1000,
  };

  puppeteer.launch(chromeOptions).then(async (browser) => {
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 720 });

    await page.goto("https://stocktwits.com/signin?next=/UpgradeDowngrade");

    await page.waitFor(Math.random() * (3000 - 1000) + 4000);

    //input username
    const username = await page.$x(
      '//*[@id="Layout"]/div[1]/div[3]/div/div[2]/form/div[1]/input'
    );
    username[0].type(process.env.USERNAME);

    // Wait for the page to load
    await page.waitFor(Math.random() * (3000 - 1000) + 1000);

    //input password
    const password = await page.$x(
      '//*[@id="Layout"]/div[1]/div[3]/div/div[2]/form/div[2]/input'
    );
    password[0].type(process.env.PASSWORD);

    // await page.screenshot({
    //   path: 'screenshot1.jpg'
    // });
    // capcha solved
    //await page.solveRecaptchas();

    await page.waitFor(5000);

    // Login
    const logginbtn = await page.$x(
      `//*[@id="Layout"]/div[1]/div[3]/div/div[2]/form/button`
    );
    logginbtn[0].click();

    await page.waitForNavigation();
    await page.waitFor(Math.random() * (3000 - 1000) + 1000);

    // Generate file queue
    const queue = fs
      .readFileSync("../../data/Queue/Queue.json", "utf8")
      .split("\n");

    // post tweets
    try {
      for (const rating of queue) {
        await page.goto("https://stocktwits.com/UpgradeDowngrade");
        let ratingObject = await JSON.parse(rating);
        let message = `$${ratingObject.Ticker} ${ratingObject.Rating.Organization} has altered their rating of "${ratingObject.Rating.Rating_Change}" see updated analyst outlook`;

        const post = await page.$x(
          '//*[@id="sidebar_top_nav_id"]/div/nav/div[1]/button'
        );
        await post[0].click();

        for (let i = 0; i < 25; i++) {
          await page.keyboard.press("Backspace");
        }

        for (let i = 0; i < message.length; i++) {
          await page.keyboard.press(message[i]);
        }

        const inputbtn = await page.$x(
          "/html/body/div[5]/div/div/div/div[2]/div/div/div/div/div[3]/div[2]"
        );
        await inputbtn[0].click();

        const elementHandle = await page.$("input[type=file]");

        await elementHandle.uploadFile(`./tweets/${ratingObject.Ticker}.png`);

        await page.waitFor(Math.random() * (3000 - 1000) + 1000);

        const postButton = await page.$x(
          "/html/body/div[5]/div/div/div/div[2]/div/div/div/div/div[5]/div/button/span"
        );
        await postButton[0].click();

        await page.waitFor(Math.random() * (3000 - 1000) + 4000);
      }
    } catch (error) {
      console.log(error);
    }
  });
})();
