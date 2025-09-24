from typing import Annotated
from rxxxt.asgi import Composer, HTTPContext, http_handler, routed_handler
from rxxxt import App, Component, El, PageBuilder, WithRegistered, event_handler, local_state, class_map, Element
from samsung_remote.utils import samsung_tv_connect
import asyncio, uvicorn, logging, websockets, os, json, importlib.resources

logging.basicConfig(level=logging.DEBUG)

class RemoteAPI:
  BUTTON_CODES: list[tuple[str, str]] = [
    ("KEY_MENU", "MENU"),
    ("KEY_LEFT", "LEFT"),
    ("KEY_RIGHT", "RIGHT"),
  ]

  def __init__(self, hostname: str) -> None:
    self._hostname = hostname
    self._command_lock = asyncio.Lock()
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
    if not self.connected:
      self._connection = await samsung_tv_connect("webremote", self._hostname, None)
      _ = await self._connection.recv()
    if self._connection is None: raise RuntimeError("Failed to connect!")
    return self._connection

def icon(name: str):
  return El.span(_class="icon", content=[name])

class Remote(Component):
  last_key = local_state(str)

  @property
  def remote_api(self):
    return self.context.registered("remote_api", RemoteAPI)

  @event_handler()
  async def send_key(self, code: str):
    self.last_key = code
    await self.remote_api.send_remote_code(code)

  @event_handler()
  async def on_key_down(self, code: Annotated[str, "code"]):
    code_map: dict[str, str] = {
      "ArrowLeft": "KEY_LEFT",
      "ArrowRight": "KEY_RIGHT",
      "ArrowUp": "KEY_UP",
      "ArrowDown": "KEY_DOWN",
      "Enter": "KEY_ENTER",
      "Escape": "KEY_RETURN",
    } | { f"Digit{d}": f"KEY_{d}" for d in range(10) }
    if (tvcode:=code_map.get(code)) is not None:
      await self.send_key(tvcode)

  def render_button(self, code: str, label: str | Element, *, small: bool = False):
    return El.div(_class=class_map({
        "remote-button": True,
        "remote-button--active": code == self.last_key,
        "remote-button--small": small
      }),
      onclick=self.send_key.bind(code=code), content=[ label ])

  async def on_init(self) -> None:
    asyncio.create_task(self.remote_api.ensure_connection())
    self.context.add_window_event("keydown", self.on_key_down)

  def render(self):
    return El.div(_class="remote-main-container", content=[
      *((El.div(),)*2),
      self.render_button("KEY_POWER", icon("power_settings_new")),
      *((El.div(),)*3),

      El.div(),
      self.render_button("KEY_UP", icon("keyboard_arrow_up")),
      El.div(),

      self.render_button("KEY_LEFT", icon("keyboard_arrow_left")),
      self.render_button("KEY_ENTER", ""),
      self.render_button("KEY_RIGHT", icon("keyboard_arrow_right")),

      El.div(),
      self.render_button("KEY_DOWN", icon("keyboard_arrow_down")),
      El.div(),

      *((El.div(),)*3),

      self.render_button("KEY_RETURN", icon("arrow_back")),
      self.render_button("KEY_HOME", icon("home")),
      self.render_button("KEY_MENU", icon("menu")),

      self.render_button("KEY_MUTE", icon("volume_mute")),
      self.render_button("KEY_VOLDOWN", icon("volume_down")),
      self.render_button("KEY_VOLUP", icon("volume_up")),

      El.div(_class="remote-inline-cell", content=[
        self.render_button(f"KEY_{d}", str(d), small=True) for d in range(10)
      ])
    ])


async def run_web():
  remote_api = RemoteAPI(os.getenv("WS_CLIENT_HOST"))

  with importlib.resources.path("samsung_remote.assets") as assets_dir:
    assets_dir_abs = str(assets_dir.absolute())

    page_builder = PageBuilder()
    page_builder.add_stylesheet("/assets/main.css")

    composer = Composer()

    @composer.add_handler
    @http_handler
    @routed_handler("/assets/{path*}")
    async def _(context: HTTPContext, params: dict[str, str]):
      asset_path_abs = assets_dir.joinpath(params["path"]).absolute()
      if os.path.commonpath([ asset_path_abs, assets_dir_abs ]) != assets_dir_abs:
        return await context.respond_text("not authorized", 403)
      return await context.respond_file(asset_path_abs, handle_404=True, use_last_modified=True)

    _ = composer.add_handler(App(lambda: WithRegistered({ "remote_api": remote_api }, Remote()), page_factory=page_builder))

    config = uvicorn.Config(app=composer, port=8004)
    await uvicorn.Server(config).serve()

if __name__ == "__main__":
  asyncio.run(run_web())
