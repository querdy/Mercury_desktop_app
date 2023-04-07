import { app, protocol, BrowserWindow } from 'electron'
import { createProtocol } from 'vue-cli-plugin-electron-builder/lib'
import installExtension, { VUEJS3_DEVTOOLS } from 'electron-devtools-installer'
const isDevelopment = process.env.NODE_ENV !== 'production'
const path = require('path')

// Scheme must be registered before the app is ready
protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { secure: true, standard: true } }
])

async function createWindow() {
  // Create the browser window.
  const win = new BrowserWindow({
    width: 1000,
    height: 600,
    resizable: false,
    autoHideMenuBar: true,
    webPreferences: {
      nodeIntegration: process.env.ELECTRON_NODE_INTEGRATION,
      contextIsolation: !process.env.ELECTRON_NODE_INTEGRATION,
    },
  })

  function pythonBackend() {
    const { PythonShell } = require('python-shell');

    let options = {
      pythonPath: './python310/python.exe',
    };

    PythonShell.run('./backend/main.py', options, function (err, results) {
      if (err) throw err;
      console.log('response: ', results);
    });
  }

  pythonBackend()

  if (process.env.WEBPACK_DEV_SERVER_URL) {
    await win.loadURL(process.env.WEBPACK_DEV_SERVER_URL)
    if (!process.env.IS_TEST) win.webContents.openDevTools()
  } else {
    createProtocol('app')
    await win.loadURL('app://./index.html')
  }
}

// Quit when all windows are closed.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow()
})

app.on('ready', async () => {
  // if (isDevelopment && !process.env.IS_TEST) {
  //   try {
  //     await installExtension(VUEJS3_DEVTOOLS)
  //   } catch (e) {
  //     console.error('Vue Devtools failed to install:', e.toString())
  //   }
  // }
  await createWindow()
})


// function pythonBackend() {
//   const { PythonShell } = require('python-shell');
//
//   let options = {
//     pythonPath: './python310/python.exe',
//   };
//
//   let python = PythonShell.run('./backend/main.py', options, function (err, results) {
//     if (err) throw err;
//     console.log('response: ', results);
//   });
//   python.on('message', function (msg) {
//     // received a message sent from the Python script (a simple "print" statement)
//     console.log(msg);
//     win.webContents.send('kekws', {'msg': msg})
//   });
// }
//
// pythonBackend()

if (isDevelopment) {
  if (process.platform === 'win32') {
    process.on('message', (data) => {
      if (data === 'graceful-exit') {
        app.quit()
      }
    })
  } else {
    process.on('SIGTERM', () => {
      app.quit()
    })
  }
}
