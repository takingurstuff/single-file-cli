import { readLines } from 'https://deno.land/std/io/mod.ts'

// Specify the Conda environment name
const condaEnvName = 'scraper'

// Specify the Python script you want to run
const scriptToRun = './pylibs/main.py'

// Function to spawn the Python process
async function spawnPythonProcess () {
  console.log('Spawning Python process...')

  const command = new Deno.Command('conda', {
    args: ['run', '-n', condaEnvName, 'python', scriptToRun],
    stdout: 'piped',
    stderr: 'piped'
  })

  const process = command.spawn()

  // Handle stdout
  ;(async () => {
    for await (const chunk of process.stdout) {
      console.log(new TextDecoder().decode(chunk))
    }
  })()

  // Handle stderr
  ;(async () => {
    for await (const chunk of process.stderr) {
      console.error(new TextDecoder().decode(chunk))
    }
  })()

  return process
}

let pythonProcess = null

console.log("Press 'S' to spawn/respawn the Python process. Press 'Q' to quit.")

// Read from standard input
for await (const line of readLines(Deno.stdin)) {
  const input = line.trim().toLowerCase()

  if (input === 's') {
    if (pythonProcess) {
      console.log('Terminating existing Python process...')
      pythonProcess.kill('SIGTERM')
    }
    pythonProcess = await spawnPythonProcess()
  } else if (input === 'q') {
    console.log('Quitting...')
    if (pythonProcess) {
      pythonProcess.kill('SIGTERM')
    }
    Deno.exit(0)
  }
}
