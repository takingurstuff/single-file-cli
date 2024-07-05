import { initialize } from './single-file-cli-api.js'
;(async () => {
  console.log('starting download engine')
  const engine = await initialize()
  console.log('download engine started, awaiting user login')
  console.log('reading and parsing urls file')
  let urls = await Deno.readTextFile('urls.txt')
  urls = urls.split(/\n/)
  console.log('list of urls to download:', urls)
  console.log('starting download')
  await engine.capture(urls)
  console.log('capture page sucessful, cleaning up')
  await engine.finish()
})()
