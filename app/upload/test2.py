from sqlalchemy_declarative2 import ImagesData, Base
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table
from sqlalchemy import MetaData

engine = create_engine('sqlite:///sqlalchemy_database.db')
Base.metadata.bind = engine

DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()
# Make a query to find all Persons in the database
session.query(ImagesData).all()
person = session.query(ImagesData).first()
print(person.startdate)

inspector = inspect(engine)

for table_name in inspector.get_table_names():
   for column in inspector.get_columns(table_name):
       print("Column: %s" % column['name'])