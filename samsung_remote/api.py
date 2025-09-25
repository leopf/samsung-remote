import asyncio, websockets, json, logging
from samsung_remote.utils import samsung_tv_connect

class RemoteAPI:
  def __init__(self, hostname: str, token: str | None) -> None:
    self._hostname = hostname
    self._token = token
    self._command_lock = asyncio.Lock()
    self._connect_lock = asyncio.Lock()
    self._connection: websockets.ClientConnection | None = None

  @property
  def connected(self):
    return self._connection is not None and self._connection.close_code is None

  async def send_remote_code(self, code: str):
    async with self._command_lock:
      payload = json.dumps({
        "method": "ms.remote.control",
        "params": {
          "Cmd": "Click",
          "DataOfCmd": code,
          "Option": "false",
          "TypeOfRemote": "SendRemoteKey"
        }
      })
      logging.debug(f"sending remote code: {code}")
      connection = await self.ensure_connection()
      await connection.send(payload)

  async def ensure_connection(self):
    async with self._connect_lock:
      if not self.connected:
        self._connection = await samsung_tv_connect("webremote", self._hostname, self._token)
      if self._connection is None: raise RuntimeError("Failed to connect!")
      return self._connection
