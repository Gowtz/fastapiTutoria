from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

# Type for the Users
class User(BaseModel):
    name: str
    age:int
    email:str
    DOB: Optional[str] = None

users = []

@app.get('/')
def index():
    return {'data':{
        'name':"Gowtham"
    }}

@app.get('/about')
def about():
    return {
        'page':"ABOUT",
        'route':"/about",
        'data':{
            'name':"Gowtham",
            'desc':"Good boy"
        }
    }
blogs = [
        {
            'id':1,
            'title':"Lorem 1"
        },
        
        {
            'id':2,
            'title':"Lorem 2"
        },
        {
            'id':3,
            'title':"Lorem 3"
        },
        {
            'id':4,
            'title':"Lorem 4"
        },
        {
            'id':5,
            'title':"Lorem 5"
        },
        {
            'id':6,
            'title':"Lorem 6"
        }
    ]


@app.get('/blogs')
def getAllBlogs(limit: Optional[int] = 10 ):
    if limit:
        if len(blogs) >= limit:
            return blogs[:limit]
    return blogs

@app.get('/blog/{id}')
def getBlog(id : int):
    # Find the blog by id
    for i in blogs:
        if i['id'] == id:
            return i

    # if nothing found return this error
    return {
        "error":"Nothing found",
        "id":id
    }

@app.get('/getTitle/{title}')
def getTitle(title:str):
    return {
        "Title": title
    }

@app.post('/user')
def addUser(user:User):
    users.append(user)
    return {"msg":"The users are added"}


@app.get('/getAllUsers')
def getAllUsers():
    return users