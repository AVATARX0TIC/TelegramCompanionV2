import asyncio
from companion.pluginmanager import download_plugins
import os
import re
import sys

loop = asyncio.get_event_loop()

async def install_plugins():
    if os.path.isfile("plugins.txt"):
        with open("plugins.txt", "r") as file:
            for line in file.readlines():
                to_match = re.match(
                        r"([^\/]+)\/([^\/]+)(\/([^\/]+)(\/(.*))?)?",
                        line)
                if to_match:
                    await download_plugins(
                                    user=to_match.group(1),
                                    repo=to_match.group(2),
                                    plugin=to_match.group(4))
                else:
                    await download_plugins(plugin=line)

async def init():
    await install_plugins()
    try:
        proc = await asyncio.create_subprocess_shell(sys.executable + " -m " + "companion")
        while proc:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        if proc:
            proc.kill()


if __name__ == "__main__":
    loop.run_until_complete(init())



