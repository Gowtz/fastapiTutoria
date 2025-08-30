from fastapi import APIRouter,HTTPException,status,Depends
from typing import Optional, List
from .. import schema , database, models
from sqlalchemy.orm import Session
router = APIRouter(
    prefix='blog'.
    tags=["Posts"]
)

@router.get('/posts',response_model=List[schema.ShowBlog])
def getAllPost(limit:Optional[int]=10,offset:Optional[int]= 0 ,db:Session = Depends(database.get_db)):
    if limit is None:
        limit = 10  # fallback to default if None is passed
    if(limit > 50):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="The limit is too high. Please provide a limit less than 50")
    data = db.query(models.Blog).offset(offset).limit(limit).all()
    return data

@router.get('/post/{id}',response_model=schema.ShowBlog)
def getOnePost(id:int,db:Session = Depends(database.get_db)):
    data = db.query(models.Blog).filter(models.Blog.id == id ).first()
    if not data:
        # Custom error response
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No Post Found")
    return data
        
# Custom Status Code `status_code`
@router.post('/post',status_code=status.HTTP_201_CREATED)
def createPost(post:schema.Blog ,db: Session = Depends(database.get_db)): # Db Connect
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

@router.delete('/post/{id}')
def deletePost(id:int,db:Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete()
    db.commit()
    return {"msg":f"the blog with the id {id} has been deleted"}

@router.put('/post/{id}')
def updatePost(id:int,post:schema.Blog,db:Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"THe Blog with the id {id} not found")
    blog.update({"title":post.title,'content':post.content,'author':post.author_id})
    db.commit()
    return {
        "msg":"Done",
        "data":blog
    }

