import os

from bson import CodecOptions
from motor.core import AgnosticCollection, AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorClient

import config


class DB(AsyncIOMotorClient):
	DB_NAME = os.getenv("DB_NAME")

	def __init__(self, connection: str):
		super().__init__(connection, maxPoolSize=None)

	@property
	def db(self) -> AgnosticDatabase:
		return self[type(self).DB_NAME]

	@property
	def users(self) -> AgnosticCollection:
		return self.db["users"].with_options(codec_options=CodecOptions(tz_aware=True, tzinfo=config.TIMEZONE))

	async def query_user(self, query: str):
		return self.users.find_one(filter=query)
