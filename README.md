# Am I Robot?

>access to AI is easy as air

python fastapi server with AI tools

[![License: GNU GPLv3](https://img.shields.io/badge/License-GNU%20GPLv3-yellow.svg)](https://opensource.org/license/gpl-3-0/)


## Installation

clone repository

```sh
git clone https://github.com/someuser32/ai_website
```

run install_requirements

```sh
./install_requirements
```

## Usage

run main.py

```sh
python3 main.py
```

## Environment

### Dependencies
Dependencies are in [pyproject.toml](/pyproject.toml) and in [install_requirements.bat](/install_requirements.bat)/[install_requirements.sh](/install_requirements.sh) file `torch` `torchvision` `torchaudio` `realesrgan`)

### Environment
Tested on Python 3.11.4 / Windows 11, but should work on >= Python 3.10 and other OS


### .env
You must create .env file with following keys
```env
TIMEZONE=put your timezone here

DB_NAME=put your database name here (from MongoDB)

MIDDLEWARE_SECRET=put your secret key for middleware
LOGIN_SECRET=put your secret key for login
MONGODB_SECRET=put your MongoDB conection here
```

| Key | Description | Example |
| --- | --- | --- |
| `TIMEZONE` | Name of your timezone (will be used in datetimes) | `Asia/Almaty` |
| `DB_NAME` | Name of your database from MongoDB | `infomatrix` |
| `MIDDLEWARE_SECRET` | Secret key for middleware | `aR2xJWfgNb15R7FplXtxywDGwGIBjpm0` |
| `LOGIN_SECRET` | Secret key for fastapi-login Login Manager | `nMtq2UHYFJxCLYOzN4BXb3bI89sy5RFd` |
| `MONGODB_SECRET` | Connection string from MongoDB | `mongodb://USERNAME:PASSWORD@IP:PORT` |

## Used materials in project
| Source | Description |
| --- | --- |
| [gpt4free](https://github.com/xtekky/gpt4free) | GPT 3.5 + GPT 4 |
| [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) | Upscaler |
| [haku-img](https://github.com/KohakuBlueleaf/a1111-sd-webui-haku-img/blob/main/scripts/main.py) | Sketch Maker + Color Correction |
| [Silero](https://github.com/snakers4/silero-models) | TTS + STT |