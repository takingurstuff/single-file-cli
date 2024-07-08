async function clickButtonsByClassOneAtATime (
  Runtime,
  executionContextId,
  buttonClass
) {
  // Find all buttons with the given class
  const result = await Runtime.evaluate({
    expression: `
      (function() {
        const buttons = document.querySelectorAll('.${buttonClass}');
        if (buttons.length < 2) {
          return { success: false, message: 'Less than 2 buttons found' };
        }
        return Array.from(buttons.slice(0, 2)).map(button => button.outerHTML);
      })()
    `,
    contextId: executionContextId
  })

  if (result.exceptionDetails) {
    console.error('Error in evaluate:', result.exceptionDetails)
    return false
  }

  const buttonHTMLs = result.result.value

  if (!Array.isArray(buttonHTMLs)) {
    console.error('Failed to find buttons')
    return false
  }
}
async function scrollAndClick (
  Page,
  Runtime,
  primaryTargetSelector,
  secondaryTargetSelector,
  clickSelector,
  buttonSelector,
  scrollPause = 2000,
  maxAttempts = 10000000,
  contextId = null
) {
  let attempts = 0

  while (attempts < maxAttempts) {
    attempts++

    try {
      const clickResult2 = await Runtime.evaluate({
        expression: `!!document.querySelector('${buttonSelector}')`,
        contextId
      })

      if (clickResult2.result.value) {
        console.log('preparing to click')
        await clickButtonsByClassOneAtATime(
          Runtime,
          contextId,
          '.attachment-item'
        )
      }

      // Check if the primary target element is present
      const primaryTargetResult = await Runtime.evaluate({
        expression: `!!document.querySelector('${primaryTargetSelector}')`,
        contextId
      })

      if (primaryTargetResult.result.value) {
        console.log('Primary target element found!')
        return { found: true, target: 'primary' }
      }

      // Check if the secondary target element is present
      if (secondaryTargetSelector) {
        const secondaryTargetResult = await Runtime.evaluate({
          expression: `!!document.querySelector('${secondaryTargetSelector}')`,
          contextId
        })

        if (secondaryTargetResult.result.value) {
          console.log('Secondary target element found!')
          return { found: true, target: 'secondary' }
        }
      }

      // Check if the click element is present
      const clickResult = await Runtime.evaluate({
        expression: `!!document.querySelector('${clickSelector}')`,
        contextId
      })

      if (clickResult.result.value) {
        console.log('Click element found, clicking it!')
        await Runtime.evaluate({
          expression: `document.querySelector('${clickSelector}').click()`,
          contextId
        })
        // Pause after clicking
        await new Promise(resolve => setTimeout(resolve, scrollPause))
      }

      // Scroll down
      await Runtime.evaluate({
        expression: 'window.scrollTo(0, document.body.scrollHeight)',
        contextId
      })

      // Pause after scrolling
      await new Promise(resolve => setTimeout(resolve, scrollPause))
    } catch (error) {
      console.error('Error during scroll and click:', error)
      // Wait a bit before retrying
      await new Promise(resolve => setTimeout(resolve, 1000))
    }
  }

  console.log('Max attempts reached without finding either target element')
  return { found: false }
}
