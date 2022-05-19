import asyncio
import os
import re

import aiohttp
import dotenv
import revolt
from revolt.ext import commands

dotenv.load_dotenv()


class JDBot(commands.CommandsClient):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.prefixless = False

    async def get_prefix(self, message: revolt.Message):

        extras = ["test*", "te*", "t*", "jdbot.", "jd.", "test.", "te."]

        comp = re.compile("^(" + "|".join(map(re.escape, extras)) + ").*", flags=re.I)
        match = comp.match(message.content)
        if match is not None:
            extras.append(match.group(1))

        if await self.is_owner(message.author) and self.prefixless:
            extras.append("")

        return extras


async def main():
    async with aiohttp.ClientSession() as session:
        bot = JDBot(session, os.environ["TOKEN"])
        await bot.start()


asyncio.run(main())
