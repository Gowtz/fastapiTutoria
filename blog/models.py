from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from .database import Base


class Blog(Base):
    __tablename__ = 'Blogs'
    id = Column(Integer,primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    author = relationship("User",back_populates='blogs')

class User(Base):
    __tablename__ = 'User'
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    blogs = relationship("Blogs",back_populates='author')
