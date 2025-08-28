from fastapi import FastAPI

app = FastAPI()

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
def getAllBlogs():
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