import base64, ssl
from websockets.asyncio.client import connect

def get_ws_url(name: str, hostname: str, token: str | None):
  b64_name = base64.b64encode(name.encode()).decode()
  return f"wss://{hostname}:8002/api/v2/channels/samsung.remote.control?name={b64_name}&token={token}"

def get_ssl_context() -> ssl.SSLContext:
  ctx = ssl.create_default_context()
  ctx.check_hostname = False
  ctx.verify_mode = ssl.CERT_NONE
  return ctx

async def samsung_tv_connect(name: str, hostname: str, token: str | None):
  return await connect(get_ws_url(name, hostname, token), ssl=get_ssl_context())
