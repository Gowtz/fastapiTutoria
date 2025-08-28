from fastapi import FastAPI
from typing import Optional
from . import schema
app = FastAPI()


@app.get('/posts')
def getAllPost(limit:Optional[int]=10):
    return {"msg":"Pimbiliki pilapi"}

@app.post('/newPost')
def createPost(post:schema.Blog):
    return post