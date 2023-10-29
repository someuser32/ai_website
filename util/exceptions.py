class DatabaseException(BaseException):
	pass


class UserAlreadyExistsError(DatabaseException):
	pass