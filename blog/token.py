from datetime import datetime, timedelta, timezone
from . import schema
import jwt
from jwt.exceptions import InvalidTokenError

SECRET_KEY = "22e0b02e4838917c205fec9d9449dd5d2b615da1d10b5f2ff8e56f61db7f6d65"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email= payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schema.TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception