const puppeteer = require("puppeteer-extra");

// Add stealth plugin and use defaults (all tricks to hide puppeteer usage)
const StealthPlugin = require("puppeteer-extra-plugin-stealth");
puppeteer.use(StealthPlugin());

const RecaptchaPlugin = require("puppeteer-extra-plugin-recaptcha");

// Add adblocker plugin to block all ads and trackers (saves bandwidth)
const AdblockerPlugin = require("puppeteer-extra-plugin-adblocker");
puppeteer.use(AdblockerPlugin({ blockTrackers: true }));

// import env variables
require("dotenv").config();

//import file system
const fs = require("fs");

//RecaptchaPlugin
puppeteer.use(
  RecaptchaPlugin({
    provider: {
      id: "2captcha",
      token: process.env.CAPTCHA_KEY,
    },
    visualFeedback: true, // colorize reCAPTCHAs (violet = detected, green = solved)
  })
);

// self invoking main function
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

    // Wait for the page to load
    await page.waitFor(Math.random() * (3000 - 1000) + 1000);

    // Click buttoon with inner text login
    // await page.screenshot({
    //   path: 'screenshot.jpg'
    // });
    //  const elements = await page.$x(
    //   '//*[@id="mainNavigation"]/div[3]/div/div/div[1]/button'
    // );
    // console.log(elements)
    // await elements[0].click();

    // Wait for the page to load
    await page.waitFor(Math.random() * (3000 - 1000) + 1000);

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
    const logginbtn = await page.$x(
      `//*[@id="Layout"]/div[1]/div[3]/div/div[2]/form/button`
    );
    logginbtn[0].click();

    await page.waitForNavigation();

    // Wait for the page to load
    await page.waitFor(Math.random() * (3000 - 1000) + 1000);

    // Click buttoon with inner text login
    // const elements2 = await page.$x(
    //   '//*[@id="Layout"]/div[1]/div[3]/div/div[2]/form/button'
    // );
    // await elements2[0].click();

    //   Read files from queue file and post them
    const queue = fs
      .readFileSync("../../data/Queue/Queue.json", "utf8")
      .split("\n");

    try {
      for (const rating of queue) {
        await page.goto("https://stocktwits.com/UpgradeDowngrade");
        let ratingObject = await JSON.parse(rating);
        let message = `$${ratingObject.Ticker} ${ratingObject.Rating.Organization} has altered their rating of "${ratingObject.Rating.Rating_Change}" see updated analyst outlook`;

        // click on the post button
        const post = await page.$x(
          '//*[@id="sidebar_top_nav_id"]/div/nav/div[1]/button'
        );
        await post[0].click();

        // clear text in post box
        // const box = await page.$x(

        //   `/html/body/div[5]/div/div/div/div[2]/div/div/div/div/div[2]/div/div[1]`
        // );

        for (let i = 0; i < 25; i++) {
          await page.keyboard.press("Backspace");
        }
  
        for (let i = 0; i < message.length; i++) {
          await page.keyboard.press(message[i]);
        }

        // // type message
        // await box[0].type(message);

        const inputbtn = await page.$x(
          `/html/body/div[5]/div/div/div/div[2]/div/div/div/div/div[3]/div[2]`
        );

        await inputbtn[0].click();

        const elementHandle = await page.$("input[type=file]");
        await elementHandle.uploadFile(`./tweets/${ratingObject.Ticker}.png`);

        await page.waitFor(Math.random() * (3000 - 1000) + 1000);

        const postButton = await page.$x(
          `/html/body/div[5]/div/div/div/div[2]/div/div/div/div/div[5]/div[2]/button`
        );
        await postButton[0].click();

        // await page.screenshot({
        //   path: 'screenshot3.jpg'
        // });

        //waitFor
        await page.waitFor(Math.random() * (3000 - 1000) + 4000);
      }
    } catch (error) {
      console.log(error);
    }

    console.log("Done");
  });
})();
