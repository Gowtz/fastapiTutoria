from fastapi import FastAPI,Depends,status,Response
from typing import Optional
from . import schema,models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session

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


@app.get('/posts')
def getAllPost(response:Response,limit:Optional[int]=10,offset:Optional[int]= 0 ,db:Session = Depends(get_db)):
    if(limit >= 50):
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return {
            "msg":"The limit is too high. Please provide a limit less than 50"
        }
    
    data = db.query(models.Blog).offset(offset).limit(limit).all()
    return data

@app.get('/post/{id}')
def getAllPost(id:int,response:Response,db:Session = Depends(get_db)):
    data = db.query(models.Blog).filter(models.Blog.id == id ).first()
    if not data:
        # Custom error response
        response.status_code = status.HTTP_404_NOT_FOUND
        return{
            "msg":"No Post Found"
        }
    return data
        
# Custom Status Code
@app.post('/newPost',status_code=status.HTTP_201_CREATED)
def createPost(post:schema.Blog ,db: Session = Depends(get_db)): # Db Connect
    new_blog = models.Blog(title= post.title, content=post.content,author=post.author)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog