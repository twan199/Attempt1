import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class ImagesData(Base):
    __tablename__ = 'db_concernee'
    
    pk = Column(Integer, primary_key=True)
    startdate = Column('startdate', String(10), unique=True, nullable=True)
    enddate = Column('enddate', String(10), unique=True, nullable=True)
    text = Column('text', String(255), unique=False, nullable=True)
    path = Column('path', String(255), unique=True, nullable=True)
 
engine = create_engine('sqlite:///sqlalchemy_database.db')
Base.metadata.create_all(engine)