from pydantic import BaseModel

class Blog(BaseModel):
    title: str
    author:str
    createdAt: str
    content:str