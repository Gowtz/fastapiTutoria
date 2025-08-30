from sqlalchemy import Column, String, Integer,ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer,primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
   # The Foreign Key represent the column int the parent table 
    author_id = Column(Integer,ForeignKey('user.id'))
    # The first Parameter should be the model class name and the back populates is the column name
    author = relationship("User",back_populates='blogs')

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    # The first Parameter should be the model class name and the back populates is the column name
    blogs = relationship("Blog",back_populates='author')
