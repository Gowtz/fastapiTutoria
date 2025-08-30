from fastapi import FastAPI,Depends,status,Response,HTTPException
from typing import Optional,List

from . import schema,models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext


pwd_context  = CryptContext(schemes=["bcrypt"],deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
def get_password_hash(password):
    return pwd_context.hash(password)

# Create table
models.Base.metadata.create_all(engine)

app = FastAPI()

# connect to the db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/posts',response_model=List[schema.ShowBlog],tags=['post'])
def getAllPost(limit:Optional[int]=10,offset:Optional[int]= 0 ,db:Session = Depends(get_db)):
    if(limit >= 50):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="The limit is too high. Please provide a limit less than 50")
    data = db.query(models.Blog).offset(offset).limit(limit).all()
    return data

@app.get('/post/{id}',response_model=schema.ShowBlog,tags=['post'])
def getOnePost(id:int,response:Response,db:Session = Depends(get_db)):
    data = db.query(models.Blog).filter(models.Blog.id == id ).first()
    if not data:
        # Custom error response
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No Post Found")
    return data
        
# Custom Status Code
@app.post('/newPost',status_code=status.HTTP_201_CREATED,tags=['post'])
def createPost(post:schema.Blog ,db: Session = Depends(get_db)): # Db Connect
    try: 
        user = db.query(models.User).filter(models.User.id == post.author_id).first()
        if not user:
            Exception("The user not found")
        new_blog = models.Blog(title= post.title, content=post.content,author_id =post.author_id)
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        return new_blog
    except Exception as e:
        print(f"The Error is {e}")

@app.delete('/post/{id}',tags=['post'])
def deletePost(id:int,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete()
    db.commit()
    return {"msg":f"the blog with the id {id} has been deleted"}

@app.put('/post/{id}',tags=['post'])
def updatePost(id:int,post:schema.Blog,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"THe Blog with the id {id} not found")
    blog.update({"title":post.title,'content':post.content,'author':post.author_id})
    db.commit()
    return {
        "msg":"Done",
        "data":blog
    }


@app.post('/user',response_model=schema.ShowUser,tags=['user'])
def createNewUser(request:schema.User,db:Session = Depends(get_db)):
    try:
        hashPassword = get_password_hash(request.password)
        db_user = models.User(name=request.name,email=request.email,password=hashPassword)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except Exception as e :
        print("The Exception is " , e)
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="User with this email already exists")
    return db_user

@app.get('/user/{id}',response_model=schema.ShowUser,tags=['user'])
def getUser(id:int,db:Session = Depends(get_db)):
    try:
        user =  db.query(models.User).filter(models.User.id == id).first()
        return user
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="There is something wrong inside")



