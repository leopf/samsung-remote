# Samsung Remote

Samsung Remote is a small web remote built with rxxxt so you can drive a Samsung Smart TV from your browser.

## Features
- Control the TV from a browser-based remote
- Keyboard shortcuts for quick navigation

## Quick Start
```bash
pip install git+https://github.com/leopf/samsung-remote.git
WS_CLIENT_HOST=my-tv-hostname python samsung_remote/web.py
```

## Project Layout
- `samsung_remote/web.py` – the web application
- `samsung_remote/utils.py` – helpers for building the TV websocket connection
- `samsung_remote/gettoken.py` – command-line token helper to get a pairing token when required
- `samsung_remote/assets/` – static files for the web remote (CSS and icon font)
