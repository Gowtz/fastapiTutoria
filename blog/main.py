from fastapi import FastAPI
from . import models
from .database import engine
from .router import blog, user

# Create table
models.Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(blog.router)
app.include_router(user.router)




