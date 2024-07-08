import { ensureDir, copy } from 'https://deno.land/std/fs/mod.ts'
import { join, basename } from 'https://deno.land/std/path/mod.ts'

const sitefolder = '/Volumes/T0/threads'
const tmpdls = '/Volumes/T0/sftmpdl2'

async function sort (title) {
  try {
    await ensureDir(sitefolder)

    const threadfolder = join(sitefolder, title)
    await ensureDir(threadfolder)

    const searchPath = join(tmpdls, '*.*')

    for await (const entry of Deno.readDir(tmpdls)) {
      if (entry.isFile) {
        const file_path = join(tmpdls, entry.name)
        const file_name = basename(file_path)
        const target_file_path = join(threadfolder, file_name)

        await Deno.rename(file_path, target_file_path)
        console.log(`Moved: ${file_path} to ${target_file_path}`)
      }
    }
  } catch (error) {
    console.error('An error occurred:', error)
  }
}
export { sort }

async function runPythonScript (scriptPath, condaEnv = null) {
  let command
  if (condaEnv) {
    // If a Conda environment is specified, use it
    command = ['conda', 'run', '-n', condaEnv, 'python', scriptPath]
  } else {
    // Otherwise, use the system's default Python
    command = ['python', scriptPath]
  }

  try {
    const process = Deno.run({
      cmd: command,
      stdout: 'piped',
      stderr: 'piped'
    })

    const [status, rawOutput, rawError] = await Promise.all([
      process.status(),
      process.output(),
      process.stderrOutput()
    ])

    const output = new TextDecoder().decode(rawOutput).trim()
    const error = new TextDecoder().decode(rawError).trim()

    process.close()

    if (status.success) {
      return { success: true, output }
    } else {
      console.error('Python script execution failed:')
      console.error(error)
      return { success: false, error }
    }
  } catch (err) {
    console.error('Error running Python script:', err.message)
    return { success: false, error: err.message }
  }
}

export { runPythonScript }
