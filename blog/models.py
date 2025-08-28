from sqlalchemy import Column, String, Integer
from .database import Base


class Blog(Base):
    __tablename__ = 'Blogs'
    id = Column(Integer,primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    author = Column(String)


