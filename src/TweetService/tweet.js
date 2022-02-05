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

puppeteer.launch({ headless: false }).then(async (browser) => {
  const page = await browser.newPage();
  await page.goto("https://stocktwits.com/");

  // Wait for the page to load
  await page.waitFor(Math.random() * (3000 - 1000) + 1000);

  // Click buttoon with inner text login

  const elements = await page.$x(
    '//*[@id="mainNavigation"]/div[3]/div/div/div[1]/button'
  );
  await elements[0].click();

  // Wait for the page to load
  await page.waitFor(Math.random() * (3000 - 1000) + 1000);

  //input username
  const username = await page.$x(
    '//*[@id="app"]/div/div/div[4]/div[2]/div/form/div[1]/div[1]/label/input'
  );
  username[0].type(process.env.USERNAME);

  // Wait for the page to load
  await page.waitFor(Math.random() * (3000 - 1000) + 1000);

  //input password
  const password = await page.$x(
    '//*[@id="app"]/div/div/div[4]/div[2]/div/form/div[1]/div[2]/label/input'
  );
  password[0].type(process.env.PASSWORD);

  // CAPCHA problem need manual validation
  // const frame = await page.frames().find(f => f.name().startsWith("a-"));
  // await frame.waitForSelector('div.recaptcha-checkbox-border').click();
  // console.log("Captcha clicked exists!");

  await page.waitForNavigation();

  // Wait for the page to load
  await page.waitFor(Math.random() * (3000 - 1000) + 1000);

  //   Read files from queue file and post them
  const queue = fs
    .readFileSync("../../data/Queue/Queue.json", "utf8")
    .split("\n");

  try {
    for (const rating of queue) {
      let ratingObject = await JSON.parse(rating);
      let message = `$${ratingObject.Ticker} ${ratingObject.Rating.Organization} has changed rating to ${ratingObject.Rating.Rating} with a price target change of ${ratingObject.Rating.Target_Change}`;

      console.log(message);

      const post = await page.$x('//*[@id="mainNavigation"]/div[3]/span/button');
      await post[0].click();
      const box = await page.$x('//*[@id="app"]/div/div/div[4]/div[2]/div/div[2]/div/div[2]/input')
      console.log(box);
      box[0].type(message);
      break;
    }
  } catch (error) {
    console.log(error);
  }

  console.log("Done");
});
