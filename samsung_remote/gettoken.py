import argparse, asyncio, json
from samsung_remote.utils import samsung_tv_connect

async def run_gettoken():
  parser = argparse.ArgumentParser()
  _ = parser.add_argument("--host", "-H", type=str, required=True)
  _ = parser.add_argument("--name", "-N", type=str, default="webremote")

  args = parser.parse_args()

  async with await samsung_tv_connect(args.name, args.host, None) as connection:
    response = await connection.recv()
    response_data = json.loads(response)
    if response_data["event"] != "ms.channel.connect":
      raise RuntimeError("Failed to connect to tv!", response_data)
    print("token:", response_data["data"]["token"])

if __name__ == "__main__":
  asyncio.run(run_gettoken())
