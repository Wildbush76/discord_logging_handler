import asyncio
from logging import getLogger

import discord

from .base_discord_handler import BaseDiscordHandler


class UserLogHandler(BaseDiscordHandler):
    def __init__(self, discord_client: discord.Client, target_user_id: int):
        self._client: discord.Client = discord_client
        self._target_user: discord.User | None = None
        self._logger = getLogger(UserLogHandler.__name__)

        asyncio.create_task(self._setup(target_user_id))

        super().__init__()

    async def _setup(self, target_user_id: int):
        try:
            self._target_user = await self._client.fetch_user(target_user_id)
        except discord.NotFound:
            self._logger.error(
                f"User : {target_user_id} could not be found for logging!"
            )
        except discord.HTTPException:
            self._logger.error("Failed to fetch user for logger!")

    async def _send_message(self, embed: discord.Embed):
        if self._target_user is None or self._client.is_closed():
            return

        await self._target_user.send(embed=embed)
