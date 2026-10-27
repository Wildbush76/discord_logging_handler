import asyncio
from logging import getLogger

import discord

from .base_discord_handler import BaseDiscordHandler


class ChannelLogHandler(BaseDiscordHandler):
    def __init__(self, discord_client: discord.Client, target_channel_id: int):
        self._client: discord.Client = discord_client
        self._target_channel: discord.User | None = None
        self._logger = getLogger(ChannelLogHandler.__name__)

        asyncio.create_task(self._setup(target_channel_id))

        super().__init__()

    async def _setup(self, target_channel_id: int):
        try:
            if self._client.is_closed():
                self._logger.error(
                    "Client not connected! Cannot retrieve logging channel"
                )
                return

            self._target_channel = self._client.fetch_channel(target_channel_id)
        except discord.NotFound:
            self._logger.error(
                f"Channel : {target_channel_id} could not be found for logging!"
            )
        except discord.HTTPException:
            self._logger.error("Failed to fetch channel for logger!")

    async def _send_message(self, embed: discord.Embed):
        if self._target_channel is None or self._client.is_closed():
            return

        await self._target_channel.send(embed=embed)
