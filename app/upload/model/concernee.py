from app import db
from app import ma

from marshmallow import fields

class Concernee(db.Model):
    """
    A person concerned by SOPs
    """
    __tablename__ = 'db_concernee'
    pk = db.Column('pk', db.Integer, primary_key=True)
    # sk = db.Column('sk', db.CHAR(16), unique=True, nullable=False)

    startdate = db.Column('startdate', db.String(10), unique=True, nullable=True, primary_key=True)
    enddate = db.Column('enddate', db.String(10), unique=True, nullable=True)
    text = db.Column('text', db.String(255), unique=False, nullable=True)
    path = db.Column('path', db.String(255), unique=True, nullable=True)

class ConcerneeSchema(ma.ModelSchema):

    class Meta:
        model = Concernee
        # exclude = ['pk']
        
    sk = fields.String(data_key='id', dump_only=True)
    startdate = fields.String(required=True)
    enddate = fields.String(required=True)
    text = fields.String(required=False)