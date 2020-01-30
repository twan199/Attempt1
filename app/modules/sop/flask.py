from flask import Blueprint, abort, request, Response, json
from marshmallow import ValidationError

from .model.concernee import Concernee, ConcerneeSchema

from app import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.rfc7807 import rfc7807_response
from app.guauoid import guauoid_generate

sop = Blueprint('sop', __name__, static_folder='static')


@sop.route('/concernees', methods=['GET'])
def list_concernees():

    # Pagination
    page = request.args.get(key='page', default=1, type=int)
    per_page = request.args.get(key='per_page', default=25, type=int)

    if per_page > 100:
        per_page = 100

    # Sorting
    sort_field_name = request.args.get(key='sort', default='name', type=str)
    sort_direction = request.args.get(key='order', default='asc', type=str)

    try:
        sort_field = getattr(Concernee, sort_field_name)
    except AttributeError:
        sort_field = Concernee.name

    if sort_direction.lower() == 'desc':
        sort_field = sort_field.desc()
    
    # Query
    concernees = db.session \
        .query(Concernee) \
        .order_by(sort_field) \
        .paginate(page, per_page, True) \
        .items

    schema = ConcerneeSchema(many=True)

    return schema.jsonify(concernees)


@sop.route('/concernees', methods=['POST'])
def create_concernee():

    schema = ConcerneeSchema()

    try:
        concernee = schema.load(request.json)

    except ValidationError as ve:
        return rfc7807_response(title='Input validation failed', blockers=ve.messages)

    concernee.pk = None
    concernee.sk = guauoid_generate()
        
    db.session.add(concernee)

    try:
        db.session.commit()

    except SQLAlchemyError as sqlae:

        # Failing a unique constraint will result in an integrity error
        if isinstance(sqlae, IntegrityError):
            return rfc7807_response(title='Conflict while creating resource', code=409)

        # Something else went wrong, bail out
        return rfc7807_response(title='Internal error while creating resource', code=500)

    # Return new concernee
    response = Response()
    response. status_code = 201  # Created
    response.mimetype = 'application/json'
    response.location = request.path + '/' + concernee.sk
    response.data = schema.dumps(concernee)

    return response


@sop.route('/concernees/<id>', methods=['GET'])
def read_concernee(id):

    concernee = db.session.query(Concernee).filter(Concernee.sk == id).one_or_none()

    if not concernee:
        return rfc7807_response(title='Resource not found', code=404)

    schema = ConcerneeSchema()
    return schema.jsonify(concernee)


@sop.route('/concernees/<id>', methods=['PATCH', 'PUT'])
def update_concernee(id):

    concernee = db.session.query(Concernee).filter(Concernee.sk == id).one_or_none()

    if not concernee:
        return rfc7807_response(title='Resource not found', code=404)

    schema = ConcerneeSchema()

    # Change existing record
    if request.method == 'PATCH':
        try:
            schema.load(request.json, instance=concernee, partial=True)
        except ValidationError as ve:
            return rfc7807_response(title='Input validation failed', blockers=ve.messages)

    # Replace record with new one
    elif request.method == 'PUT':
        try:
            schema.load(request.json, instance=concernee, partial=False)
        except ValidationError as ve:
            return rfc7807_response(title='Input validation failed', blockers=ve.messages)

    else:
        abort(500)

    # Try update
    try:
        db.session.commit()
    except SQLAlchemyError as sqlae:

        # Failing a unique constraint will result in an integrity error
        if isinstance(sqlae, IntegrityError):
            return rfc7807_response(title='Conflict while updating resource', code=409)

        # Something else went wrong, bail out
        return rfc7807_response(title='Internal error while creating resource', code=500)

    # Return current resource
    return schema.jsonify(concernee)


@sop.route('/concernees/<id>', methods=['DELETE'])
def delete_concernee(id):

    concernee = db.session.query(Concernee).filter(Concernee.sk == id).one_or_none()

    if not concernee:
        return rfc7807_response(title='Resource not found', code=404)

    db.session.delete(concernee)

    try:
        db.session.commit()
    except SQLAlchemyError as sqlae:
        return rfc7807_response(title='Internal error while deleting resource', code=500)

    response = Response()
    response.status_code = 204  # No content ...
    del response.content_type   # .. no type ♫
    
    return response