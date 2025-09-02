from fastapi import FastAPI
from . import models
from .database import engine
from .router import blog, user,auth
from  dotenv import load_dotenv

# Create table
models.Base.metadata.create_all(engine)
load_dotenv()
app = FastAPI()

app.include_router(blog.router)
app.include_router(user.router)
app.include_router(auth.router)




