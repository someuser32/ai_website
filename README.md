# Am I robot? | AIr

[Description](https://github.com/someuser32/ai_website/blob/main/pyproject.toml)

# Environment

## Dependencies
Dependencies are in pyproject.toml

## Environment
Tested on Python 3.11.4 / Windows 11, but should work on >= Python 3.10 and other OS

### .env
You must create .env file with following keys

```env
TIMEZONE=put your timezone here

DB_NAME=put your database name here (from MongoDB)

MIDDLEWARE_SECRET=put your secret key for middleware
LOGIN_SECRET=put your secret key for login
MONGODB_CONNECTION=put your MongoDB conection here
```

| Key | Description | Example |
| --- | --- | --- |
| `TIMEZONE` | Name of your timezone (will be used in datetimes) | `Asia/Almaty` |
| `DB_NAME` | Name of your database from MongoDB | `infomatrix` |
| `MIDDLEWARE_SECRET` | Secret key for middleware | `aR2xJWfgNb15R7FplXtxywDGwGIBjpm0` |
| `LOGIN_SECRET` | Secret key for fastapi-login Login Manager | `nMtq2UHYFJxCLYOzN4BXb3bI89sy5RFd` |
| `MONGODB_CONNECTION` | Secret key for fastapi-login Login Manager | `mongodb://USERNAME:PASSWORD@IP:PORT` |