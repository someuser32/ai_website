import os
from contextlib import suppress as except_error
from typing import Iterable, Any

from bson import CodecOptions
from deepdiff import DeepDiff
from motor.core import AgnosticCollection, AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorClient

import util.config as config
from .user import User
from .lib import parse_deepdiff_keys, recursively_setvalue_from, recursively_removekey, recursively_setvalue, recursively_getvalue, safe_typecast


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

	async def query_user(self, query: str) -> User:
		user_data = await self.users.find_one(filter=query)
		if user_data is None:
			return None
		del user_data["_id"]
		default_user = await self.users.find_one(filter={"__is_default": True})
		user_data = await self.sync_user(user_data, )
		return User(data=user_data)

	async def update_user(self, user: User):
		changes = set()
		await self.users.update_one({"username": user.username}, {"$set": user.__dict__})

	@staticmethod
	def sync_user_data(data: dict, default_data: dict, exceptions: Iterable[str]=None) -> dict | None:
		if exceptions is None:
			exceptions = ()
		diff = DeepDiff(data, default_data)
		if not any(info for info in diff if info in ("dictionary_item_removed", "dictionary_item_added", "type_changes")):
			return None
		new_data = data.copy()
		if added := diff.get("dictionary_item_added"):
			for add in added:
				keys = parse_deepdiff_keys(add)
				if isinstance(keys[-1], str) and keys[-1].startswith("__"):
					continue
				recursively_setvalue_from(new_data, default_data, keys)
		if removed := diff.get("dictionary_item_removed"):
			for rem in removed:
				recursively_removekey(new_data, parse_deepdiff_keys(rem))
		if typechanges := diff.get("type_changes"):
			for tchange in typechanges.keys():
				keys = parse_deepdiff_keys(tchange)
				old, new = recursively_getvalue(new_data, keys), recursively_getvalue(default_data, keys)
				recursively_setvalue(new_data, safe_typecast(old, new), keys)
		return new_data

	async def sync_user(self, user: dict, default_user: dict) -> dict | None:
		if new_user := type(self).sync_user_data(data=user, default_data=default_user):
			await self.users.update_one({"username": user["username"]}, {"$set": new_user})
			return new_user
		return None
