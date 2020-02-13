from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from sqlalchemy_declarative2 import Base, ImagesData
 
engine = create_engine('sqlite:///sqlalchemy_database.db')
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# session.rollback()
session = DBSession()

new_image = ImagesData(
	startdate='2015.32.25',
	enddate='2020.20.20',
	text='Hallooooo',
	path='cdc/csf/sdf/sdf/sdfs/df'	)
session.add(new_image)
session.commit()