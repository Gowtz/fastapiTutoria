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

