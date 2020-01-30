from app import db
from app import ma

from marshmallow import fields

class Concernee(db.Model):
    """
    A person concerned by SOPs
    """
    
    __tablename__ = 'sop_concernee'

    pk = db.Column('pk', db.Integer, primary_key=True)
    sk = db.Column('sk', db.CHAR(16), unique=True, nullable=False)

    name = db.Column('name', db.String(50), unique=False, nullable=True)
    short = db.Column('short', db.String(5), unique=True, nullable=True)

    leaving_date = db.Column('leaving_date', db.Date, unique=False, nullable=True)
    has_left = db.Column('has_left', db.Boolean, unique=False, nullable=False, default=False)


class ConcerneeSchema(ma.ModelSchema):

    class Meta:
        model = Concernee
        exclude = ['pk']

    sk = fields.String(data_key='id', dump_only=True)

    name = fields.String(required=True)
    short = fields.String(required=True)
    leaving_date = fields.Date(required=False, default=None, dump_only=True)
    has_left = fields.Boolean(required=False, default=False, dump_only=True)
