import datetime
import os
from contextlib import suppress as except_error
from typing import Any, Iterable

import bcrypt
import pymongo.errors
from bson import CodecOptions
from deepdiff import DeepDiff
from motor.core import AgnosticCollection, AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorClient

import util.config as config

from .exceptions import UserAlreadyExistsError
from .lib import parse_deepdiff_keys, recursively_getvalue, recursively_removekey, recursively_setvalue, recursively_setvalue_from, safe_typecast
from .user import User


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
		default_user = await self.users.find_one(filter={"__is_default": True})
		user_data = (await self.sync_user(user_data, default_user)) or user_data
		return User(data=user_data, db=self)

	async def create_user(self, username: str, email: str, password: str) -> User:
		user = await self.query_user({"username": username})
		if user is not None:
			raise UserAlreadyExistsError(f"user {username} is already exists!")
		default_user = await self.users.find_one(filter={"__is_default": True})
		user_data = type(self).sync_user_data({"username": username, "email": email, "password_hash": bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")}, default_user)
		try:
			await self.users.insert_one(user_data)
		except pymongo.errors.DuplicateKeyError:
			raise UserAlreadyExistsError(f"user {username} is already exists!")
		return User(data=user_data, db=self)

	async def update_user(self, user: User):
		diff = DeepDiff(user.__dict__, user._persistent_data)
		new_data = user.__dict__
		if changed := diff.get("values_changed"):
			new_data = {".".join(parse_deepdiff_keys(changek)) for changek in changed.keys()}
		del new_data["_id"]
		await self.users.update_one({"username": user.username}, {"$set": new_data})

	@staticmethod
	def sync_user_data(data: dict, default_data: dict) -> dict | None:
		diff = DeepDiff(data, default_data)
		if not any(info for info in diff if info in ("dictionary_item_removed", "dictionary_item_added", "type_changes")):
			return None
		new_data = data.copy()
		if added := diff.get("dictionary_item_added"):
			for add in added:
				keys = parse_deepdiff_keys(add)
				if (isinstance(keys[-1], str) and keys[-1].startswith("__")) or keys[0] == "_id":
					continue
				recursively_setvalue_from(new_data, default_data, keys)
		if removed := diff.get("dictionary_item_removed"):
			for rem in removed:
				keys = parse_deepdiff_keys(rem)
				if keys[0] == "_id":
					continue
				recursively_removekey(new_data, keys)
		if typechanges := diff.get("type_changes"):
			for tchange in typechanges.keys():
				keys = parse_deepdiff_keys(tchange)
				old, new = recursively_getvalue(new_data, keys), recursively_getvalue(default_data, keys)
				recursively_setvalue(new_data, safe_typecast(old, new), keys)
		return new_data

	async def sync_user(self, user_data: dict, default_user: dict) -> dict | None:
		if new_user := type(self).sync_user_data(data=user_data, default_data=default_user):
			await self.users.update_one({"username": user_data["username"]}, {"$set": new_user})
			return new_user
		return None
