import asyncio
import re
from aiohttp import ClientSession

from ZeroTwo import ARQ_API
from ZeroTwo import telethn as ZeroTwo

from Python_ARQ import ARQ

aiohttp_session = ClientSession()
arq = ARQ(ARQ_URL, ARQ_API, aiohttp_session)

async def getresp(query: str, user_id: int):
  bot = await arq.bot(query, user_id)
  response = bot.result
  return response

@ZeroTwo.on_message(filters.command(
