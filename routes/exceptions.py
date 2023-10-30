from fastapi.exceptions import HTTPException

IncorrectCaptchaException = HTTPException(status_code=400, detail="Invalid captcha answer!", headers={"WWW-Authenticate": "Bearer"})
UsernameExistsException = HTTPException(status_code=400, detail="This username is used by another!", headers={"WWW-Authenticate": "Bearer"})
InvalidEmailException = HTTPException(status_code=400, detail="Invalid email!", headers={"WWW-Authenticate": "Bearer"})