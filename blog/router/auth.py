from fastapi import APIRouter,Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from .. import  database,models,hash,token
from sqlalchemy.orm import Session
from ..schema import Token
router = APIRouter(tags=['auth'])



@router.post('/login')
def login(request:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(database.get_db))->Token:
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found")
    if not hash.verify_password(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid Password")

    # Generate Token


    access_token = token.create_access_token(
        data={"sub": user.email}
    )
    return Token(access_token=access_token, token_type="bearer")


