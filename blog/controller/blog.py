from fastapi import HTTPException,status
from sqlalchemy.orm import Session
from .. import models,schema

def getAll(limit:int, offset:int, db:Session):
    try:
        if(limit > 50):
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="The limit is too high. Please provide a limit less than 50")
        data = db.query(models.Blog).offset(offset).limit(limit).all()
    except Exception as e:
        print(f"\n\n\n The Exceptions is {e} \n\n\n")
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Something went wrong")
    return data

def getPost(id:int,db:Session):

    data = db.query(models.Blog).filter(models.Blog.id == id ).first()
    if not data:
        # Custom error response
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No Post Found")

def createPost(post:schema.Blog,db:Session):
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

def deletePost(id:int,db:Session):
    try:
        db.query(models.Blog).filter(models.Blog.id == id).delete()
        db.commit()
    except Exception as e:
        print(f"\n\n\n The Exception is {e} \n\n\n")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Somthin went wrong")
    return {"msg":f"the blog with the id {id} has been deleted"}

def updatePost(id:int,post:schema.Blog , db:Session):
    try:
        blog = db.query(models.Blog).filter(models.Blog.id == id)
        if not blog.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"THe Blog with the id {id} not found")
        blog.update({"title":post.title})
        db.commit()
    except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"{e}")
    return {
        "msg":"Done",
        "data":blog
    }
