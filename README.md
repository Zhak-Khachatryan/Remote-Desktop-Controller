# Phone-to-Laptop Controller

A simplistic application for controlling your laptop using your phone through a locally hosted website.

The project is built with **Angular** for the frontend and **Flask** for the backend. It is designed to let your phone act like a remote control for your computer on the same local network.

## Overview

This project provides a lightweight way to send basic input events from a phone to a laptop. The frontend runs in the browser on your phone, while the backend listens locally on your Windows machine and translates requests into mouse and keyboard actions.

It is intended to be simple, fast, and easy to understand. The codebase is also a good starting point for anyone who wants to build a custom remote control, game controller, touchpad, or automation interface.

## Features

* Control your laptop from a phone over a local network
* Send keyboard input from the browser
* Support for key hold and key release actions
* Mouse click support
* Mouse movement support
* Simple local API powered by Flask
* Angular-based user interface
* Easy to extend with new controls and commands

## Requirements

* **Windows** operating system
* **Python** installed
* **JavaScript / Node.js** installed
* A phone and laptop connected to the **same network**
* A modern browser on the phone

## Initialization

### FRONTEND
Start-Process powershell -ArgumentList "cd .\Phone-Frontend; npm install"

### BACKEND
Start-Process powershell -ArgumentList "cd .\PC-Backend; pip install uv; uv venv venv; .venv/Scripts/Activate; uv pip install -r requirements.txt"

## Execution

### FRONTEND
Start-Process powershell -ArgumentList "cd .\Phone-Frontend; ng serve --host 0.0.0.0"

### BACKEND 
Start-Process powershell -ArgumentList "cd .\PC-Backend; .venv/Scripts/Activate; python server.py"

## NOTE: Make sure to change the url on the Phone-Frontend/src/app/app.ts to the corresponding url in order for the Frontend to be able to successfully communicate with the Backend

### Planned steps

1. Clone the repository
2. Install backend dependencies
3. Install frontend dependencies
4. Build or run the Angular app
5. Start the Flask backend
6. Open the frontend on your phone
7. Connect to the laptop using the local IP address

## How it works

The system is split into two parts:

### Frontend

The Angular frontend is opened on your phone. It acts as the control panel and sends requests to the backend when you tap buttons, drag sliders, or trigger other actions.

### Backend

The Flask backend runs on the laptop. It receives HTTP requests from the frontend and converts them into real input events such as keyboard presses, mouse clicks, and pointer movement.

## Usage

Once the app is running, open the website from your phone using the laptop's local IP address. From there, you can interact with the controls and send commands to the backend.

Typical actions may include:

* Pressing movement keys like `W`, `A`, `S`, and `D`
* Holding a key down for continuous movement
* Clicking mouse buttons
* Moving the cursor with touch input
* Sending quick actions or shortcuts

## Project Structure

A typical structure may look like this:

```bash
project-root/
├── PC-BACKEND/
│   ├── server.py
│   └── requirements.txt
├── Phone-Frontend/
│   ├── src/
|   |   └── app/
|   |       └── app.ts
│   ├── angular.json
│   └── package.json
├── .gitignore
└── README.md
```

## Why this project exists

This project is useful as a personal remote-control tool and as a learning project. It combines frontend development, backend API design, device communication, and operating-system-level input automation.

It can also be used as a foundation for more advanced features later, such as:

* Custom key mappings
* A virtual touchpad
* Volume control
* Media controls
* Game-specific layouts
* Shortcuts and macros
* Connection status indicators
* Authentication for local network safety

## Notes

* This project is designed for local use.
* It currently requires Windows because it relies on Windows input handling.
* Some functionality may depend on browser permissions and local network access.
* The backend should only be exposed carefully if security is added later.

## Future Improvements

* Add screenshots
* Add support for more input types
* Improve mobile UI design

## Troubleshooting

### The phone cannot connect

Make sure both devices are on the same Wi-Fi network and that the backend is running on the correct host and port.

### Inputs are not working

Check that the Flask backend is running with the correct permissions and that the browser can reach the backend endpoint.

### The page does not load

Verify the frontend build, the local IP address, and any firewall settings that may block access.

## Disclaimer

This project is meant for personal and local use. Be careful when exposing it to networks you do not trust.
