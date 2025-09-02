from fastapi import APIRouter,HTTPException,status,Depends
from .. import schema,models,database,hash
from sqlalchemy.orm import Session


# SetUp Router
router = APIRouter(
    tags=["Users"]
)

@router.post('/user',response_model=schema.ShowUser)
def createNewUser(request:schema.User,db:Session = Depends(database.get_db)):
    try:
        hashPassword = hash.get_password_hash(request.password)
        db_user = models.User(name=request.name,email=request.email,password=hashPassword)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e :
        print("The Exception is " , e)
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="User with this email already exists")
    return db_user

@router.get('/user/{id}',response_model=schema.ShowUser)
def getUser(id:int,db:Session = Depends(database.get_db)):
    try:
        user =  db.query(models.User).filter(models.User.id == id).first()
        return user
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="There is something wrong inside")



