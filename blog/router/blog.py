from fastapi import APIRouter,HTTPException,status,Depends,Query
from typing import List
from .. import schema , database, models
from ..controller import blog
from sqlalchemy.orm import Session
from ..Oauth2 import get_current_user

router = APIRouter(
    prefix='/blog',
    tags=["Posts"]
)

@router.get('/posts',response_model=List[schema.ShowBlog])
def getAllPost(
    limit: int = Query(default=10, le=50),
    offset: int = Query(default=0, ge=0),
    db:Session = Depends(database.get_db),get_current_user:schema.User = Depends(get_current_user)
):
    return blog.getAll(limit,offset,db)

@router.get('/post/{id}',response_model=schema.ShowBlog)
def getOnePost(id:int,db:Session = Depends(database.get_db)):
    return blog.getPost(id,db)
        
# Custom Status Code `status_code`
@router.post('/post',status_code=status.HTTP_201_CREATED)
def createPost(post:schema.Blog ,db: Session = Depends(database.get_db)): # Db Connect
    return blog.createPost(post,db)

@router.delete('/post/{id}')
def deletePost(id:int,db:Session = Depends(database.get_db)):
    return blog.deletePost(id,db)

@router.put('/post/{id}')
def updatePost(id:int,post:schema.Blog,db:Session = Depends(database.get_db)):
    return blog.updatePost(id,post,db)
