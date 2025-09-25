# Samsung Remote

Samsung Remote is a small web remote built with rxxxt to drive a Samsung Smart TV from the browser.

## Features
- Control the TV from the browser
- Use shortcuts for quick navigation

## Quick Start
```bash
pip install git+https://github.com/leopf/samsung-remote.git
TV_HOST=my-tv-hostname TV_TOKEN=my-tv-token python samsung_remote/web.py
```

- `TV_HOST` (required): hostname or IP address of your TV.
- `TV_TOKEN` (optional): pairing token. Leave it unset on the first run to obtain one.

When `TV_TOKEN` is not provided, the application triggers the TV's pairing prompt. After you accept the prompt on the TV, the terminal prints `token: <value>`. Copy that value and export it as `TV_TOKEN` for future runs so you can connect without re-approving the pairing.

## Project Layout
- `samsung_remote/web.py` – the web application
- `samsung_remote/api.py` – samsung api
- `samsung_remote/utils.py` – helpers for building the TV websocket connection and printing the pairing token after the first connection
- `samsung_remote/assets/` – static files for the web remote (CSS and icon font)
