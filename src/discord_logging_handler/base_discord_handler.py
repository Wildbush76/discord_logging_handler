import asyncio
from abc import ABC, abstractmethod
from logging import Handler, LogRecord
from typing import override

import discord
from discord import Embed
from ratelimit import limits, sleep_and_retry


class BaseDiscordHandler(Handler, ABC):
    @abstractmethod
    async def _send_message(self, embed: discord.Embed):
        pass

    @override
    def emit(self, record: LogRecord) -> None:
        asyncio.create_task(self._send_record(record))

    async def info(self, title: str, message: str):
        await self._send_message(
            Embed(title=title, description=message, color=discord.Color.blue())
        )

    async def warning(self, title: str, message: str):
        await self._send_message(
            Embed(title=title, description=message, color=discord.Color.yellow())
        )

    async def error(self, title: str, message: str):
        await self._send_message(
            Embed(title=title, description=message, color=discord.Color.red())
        )

    async def critical(self, title: str, message: str):
        await self._send_message(
            Embed(title=title, description=message, color=discord.Color.dark_red())
        )

    @sleep_and_retry
    @limits(calls=5, period=1)
    async def _send_record(self, record: LogRecord) -> None:

        title = f"{record.name}:{record.levelname}"
        description = record.message

        if record.exc_text is not None:
            description += f" -> {record.exc_text}"

        match record.levelname.upper():
            case "INFO":
                await self.info(title, description)
            case "WARNING":
                await self.warning(title, description)
            case "ERROR":
                await self.error(title, description)
            case "CRITICAL":
                await self.critical(title, description)
