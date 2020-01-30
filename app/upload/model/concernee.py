from app import db
from app import ma

from marshmallow import fields

class Concernee(db.Model):
    """
    A person concerned by SOPs
    """
    
    __tablename__ = 'db_concernee'

    startdate = db.Column('startdate', db.String(10), unique=True, nullable=True)
    enddate = db.Column('enddate', db.String(10), unique=True, nullable=True)
    text = db.Column('text', db.String(255), unique=False, nullable=True)
    path = db.Column('path', db.String(255), unique=True, nullable=True)


class ConcerneeSchema(ma.ModelSchema):

    class Meta:
        model = Concernee
    startdate = fields.String(required=True)
    enddate = fields.String(required=True)
    text = fields.String(required=False)