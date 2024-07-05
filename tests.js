import puppeteer from 'puppeteer-core'
import readline from 'readline'
var pageinfo
;(async () => {
  let browser
  try {
    browser = await puppeteer.connect({
      browserURL: 'http://localhost:9222'
    })

    const page = await browser.newPage()
    await page.goto('https://bbs.quantclass.cn')
    console.log('awaiting user login')

    try {
      await waitForEnter()
      console.log('user logged in')
    } catch (error) {
      console.error('Login confirmation failed:', error.message)
      return
    }

    // Check for the presence of the specific element
    const threadpage1 = await browser.newPage()
    await threadpage1.goto('https://bbs.quantclass.cn/thread/42532')
    const attachment = await threadpage1.$('.attachment-item')
    const specificElement = await threadpage1.$('.hide-content-tip')
    if (attachment) {
      await threadpage1.click('.attachment-item')
    }
    if (!specificElement) {
      // If the specific element is not found, continue with the rest of the code
      await scrollAndClick(threadpage1, '.no-more', '.load-more', 500, 10000000)
      await wait(60000)
    } else {
      console.log('Specific element found, skipping the rest of the code.')
    }
  } catch (error) {
    console.error('An error occurred:', error.message)
  } finally {
    if (browser) {
      await browser.disconnect()
    }
  }
})()

async function waitForEnter () {
  return new Promise((resolve, reject) => {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    })

    rl.question(
      'Press Enter to confirm login (or any other key to exit)...',
      input => {
        rl.close()
        if (input.trim() === '') {
          resolve()
        } else {
          reject(new Error('User entered a value instead of pressing Enter.'))
        }
      }
    )
  })
}

function wait (ms) {
  return new Promise(resolve => {
    setTimeout(() => resolve(), ms)
  })
}

async function scrollAndClick (
  page,
  targetSelector,
  clickSelector,
  scrollPause = 2000,
  maxAttempts = 10000000
) {
  let attempts = 0

  while (attempts < maxAttempts) {
    attempts++

    // Check if the target element is present
    const targetElement = await page.$(targetSelector)
    if (targetElement) {
      console.log('Target element found!')
      break
    }

    // Check if the click element is present
    const clickElement = await page.$(clickSelector)
    if (clickElement) {
      console.log('Click element found, clicking it!')
      await clickElement.click()
      // Pause after clicking
      await wait(scrollPause)
    }

    // Scroll down by a certain amount
    await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')

    // Pause after scrolling
    await wait(scrollPause)
  }
}
