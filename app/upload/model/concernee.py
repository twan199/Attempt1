from app import db
from app import ma

from marshmallow import fields

class Concernee(db.Model):
    """
    A person concerned by SOPs
    """
    
    __tablename__ = 'db_concernee'

    startdate = db.Column('name', db.String(10), unique=True, nullable=True)
    enddate = db.Column('name', db.String(10), unique=True, nullable=True)
    text = db.Column('short', db.String(100), unique=False, nullable=True)
    path = db.Column('short', db.String(100), unique=True, nullable=True)


class ConcerneeSchema(ma.ModelSchema):

    class Meta:
        model = Concernee
    startdate = fields.String(required=True)
    enddate = fields.String(required=True)
    text = fields.String(required=False)