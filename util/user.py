from __future__ import annotations

import datetime
from typing import TypedDict, TYPE_CHECKING

import bcrypt

import util.config as config

if TYPE_CHECKING:
	from .db import DB


class UserSession(TypedDict):
	token: str
	ip: str
	last_used: datetime.datetime


class UserData(TypedDict):
	username: str
	email: str
	password_hash: str
	registration_date: datetime.datetime
	sessions: list[UserSession]


class User:
	def __init__(self, data: dict, db: DB):
		self._data = data
		self._persistent_data = data.copy()

	@property
	def username(self) -> str:
		return self._data.get("username", "undefined")

	@username.setter
	def username(self, new: str):
		self._data["username"] = new

	@property
	def email(self) -> str:
		return self._data.get("email", "undefined")

	@email.setter
	def email(self, new: str):
		self._data["email"] = new

	@property
	def password_hash(self) -> str:
		return self._data.get("password_hash", "undefined")

	@password_hash.setter
	def password_hash(self, new: str):
		self._data["password_hash"] = new

	def edir_password(self, new: str):
		self.password_hash = bcrypt.hashpw(new.encode("utf-8"), bcrypt.gensalt())

	@property
	def registration_date(self) -> datetime.datetime:
		return self._data.get("registration_date", datetime.datetime(year=1970, month=1, day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=datetime.timezone.utc).astimezone(config.TIMEZONE))

	@property
	def __dict__(self) -> UserData:
		return self._data
