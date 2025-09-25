import base64, ssl, json
from websockets.asyncio.client import connect

def get_ws_url(name: str, hostname: str, token: str | None):
  b64_name = base64.urlsafe_b64encode(name.encode()).decode()
  url = f"wss://{hostname}:8002/api/v2/channels/samsung.remote.control?name={b64_name}"
  if token is not None: url += f"&token={token}"
  return url

def get_ssl_context() -> ssl.SSLContext:
  ctx = ssl.create_default_context()
  ctx.check_hostname = False
  ctx.verify_mode = ssl.CERT_NONE
  return ctx

async def samsung_tv_connect(name: str, hostname: str, token: str | None):
  connection = await connect(get_ws_url(name, hostname, token), ssl=get_ssl_context())
  response = await connection.recv()
  response_data = json.loads(response)
  if response_data["event"] != "ms.channel.connect":
    raise RuntimeError("Failed to connect to tv!", response_data)
  if token is None:
    print("token:", response_data["data"]["token"])
  return connection
