from jose import JWTError,jwt
from  datetime import timedelta, datetime
from fastapi import HTTPException,status,Query
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from .database import SESSION_FACTORY



SECRET_KEY = "cc8ab5d0cc57665c0e878e414576dc88d3f422dbaa708a76cdd6b70ae9611556"
ALGORITHM = "HS256"

#exception error
Invalid_credentials_error = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#sync session
def get_db_session():
    db = SESSION_FACTORY()
    try:
        yield db
    finally:
        db.close()



#authenticate token
def auth_token(token: Annotated[str, Query()]):  #grabs token from query parameter
    try:
        id = decode_token(token)
        if id:
            return True
    except:
        return False



#hash_context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated ="auto" )


#generate access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



#decode access token
def decode_token(token):
    try:
        payload = jwt.decode(token,SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        user_id = payload.get("sub")
        if user_id is None:
            raise  Invalid_credentials_error
        return int(user_id)
    except JWTError:
        raise Invalid_credentials_error



#check password validity
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


#hash password
def hash_password(password: str):
    return pwd_context.hash(password)


def allowed_for_user_crud(user_id:int):
    pass



def allowed_for_record_crud(user_id:int):
    pass

