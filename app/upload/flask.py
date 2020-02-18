from flask import Blueprint, abort, request, Response, json, render_template, jsonify
from flask import current_app as app
from app.upload.imageprocessor import processor2
from app import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from marshmallow import ValidationError

from app.rfc7807 import rfc7807_response
from app.guauoid import guauoid_generate

from .model.concernee import Concernee, ConcerneeSchema

import magic
import hashlib
import os
import errno

upload = Blueprint('upload', __name__, static_folder='static')

@upload.route("/concernees", methods=['GET'])
def users():
    # Pagination
    page = request.args.get(key='page', default=1, type=int)
    per_page = request.args.get(key='per_page', default=25, type=int)

    if per_page > 100:
        per_page = 100
    # Query
    concernees = db.session \
        .query(Concernee) \
        .paginate(page, per_page, True) \
        .items

    schema = ConcerneeSchema(many=False)

    return schema.jsonify(concernees)

# @upload.route('/concernees', methods=['GET'])
# def list_concernees():

#     # Pagination
#     page = request.args.get(key='page', default=1, type=int)
#     per_page = request.args.get(key='per_page', default=25, type=int)

#     if per_page > 100:
#         per_page = 100

#     # Sorting
#     sort_field_name = request.args.get(key='sort', default='name', type=str)
#     sort_direction = request.args.get(key='order', default='asc', type=str)

#     try:
#         sort_field = getattr(Concernee, sort_field_name)
#     except AttributeError:
#         sort_field = Concernee.name

#     if sort_direction.lower() == 'desc':
#         sort_field = sort_field.desc()
    
#     # Query
#     concernees = db.session \
#         .query(Concernee) \
#         .order_by(sort_field) \
#         .paginate(page, per_page, True) \
#         .items

#     schema = ConcerneeSchema(many=True)

#     return schema.jsonify(concernees)

# @upload.route('/concernees', methods=['POST'])
# def upload_data():
#     schema = ConcerneeSchema()
#     try:
#         concernee = schema.load(request.json)

#     except ValidationError as ve:
#         return rfc7807_response(title='Input validation failed', blockers=ve.messages)

#     concernee.pk= None
#     concernee.sk = guauoid_generate()
    
#     db.session.add(concernee)
#     abc = Concernee(startdate='1212', enddate='123', text='dsdadas', path='234234')
#     db.session.add(abc)
#     try:
#         db.session.commit()
#     except SQLAlchemyError as sqlae:
#         # Failing a unique constraint will result in an integrity error
#         if isinstance(sqlae, IntegrityError):
#             return rfc7807_response(title='Conflict while creating resource', code=409)

#         # Something else went wrong, bail out
#         return rfc7807_response(title='Internal error while creating resource', code=500)

#     print(Concernee.query.all())
#     response = Response()
#     response. status_code = 201  # Created
#     response.mimetype = 'application/json'
#     response.location = request.path + '/' + concernee.sk
#     response.data = schema.dumps(concernee)

#     return response

# @upload.route('/api', methods=['GET'])
# def api_run():
#     return '''<h1>Distant Reading Archive</h1><p>A prototype API for distant reading of science fiction novels.</p>'''

# @upload.route('/upload', methods=['POST'])
# def upload_image():

#     images_path = os.path.join(app.instance_path, 'images')
#     os.makedirs(images_path, exist_ok=True)

#     results = []
#     # For the moment we only allow one image per upload
#     if len(request.files) != 1:
#         response = Response()
#         response.status_code = 422
#         response.mimetype = 'application/problem+json'

#         payload = {
#             'type': 'error',
#             'title': 'Only one image per request permitted'
#         }
#         response.data = json.dumps(payload)

#         return response

#     for image in request.files.values():

#         current = {}
#         results.append(current)

#         mime_type = image.mimetype.split(sep='/', maxsplit=1)[1].lower()

#         if mime_type == 'jpeg':
#             extension = 'jpg'
#         elif mime_type == 'png':
#             extension = 'png'
#         else:
#             current['type'] = 'error'
#             current['title'] = 'Dieses Format wird nicht unterstützt, JPEG oder PNG bitte'
#             continue

#         buffer = image.stream.read()
#         magic_type = magic.from_buffer(buffer).split(maxsplit=1)[0].lower()

#         if mime_type != magic_type:
#             current['type'] = 'error'
#             current['title'] = 'Irgendwas ist komisch mit dieser Datei'
#             continue

#         image_data = b''
#         sha256 = hashlib.sha256()
#         while buffer:
#             image_data += buffer
#             sha256.update(buffer)
#             buffer = image.stream.read()

#         hashname = sha256.hexdigest()
#         images_path = os.path.join(images_path, hashname)
#         os.makedirs(images_path, exist_ok=True)
#         image_path1 = os.path.join(images_path,'original')
#         try:
#             file_handle = os.open(image_path1, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
#         except OSError as exception:
#             if exception.errno == errno.EEXIST:
#                 current['type'] = 'error'
#                 current['title'] = 'Dieses Bild haben wir schon bekommen'
#                 continue
#             else:
#                 raise
#         else:
#             with os.fdopen(file_handle, 'wb') as image_file:
#                 image_file.write(image_data)
#                 processor2(images_path + "/")



#         current['type'] = 'success'

#     if results[0]['type'] == 'error':
#         response = Response()
#         response.status_code = 422
#         response.mimetype = 'application/problem+json'

#         response.data = json.dumps(results[0])

#         return response

#     elif results[0]['type'] == 'success':
#         response = Response()
#         response.status_code = 204

#         return response

#     else:
#         abort(500)

#     try:
#         return render_template("imageview.html")
#     except TemplateNotFound:
#         abort(404)

