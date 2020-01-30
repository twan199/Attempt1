"""
RFC 7807 helper functions.

Author: Joern Wittek <jwittek@biogrund.com>
"""

from flask import request, Response, json
from werkzeug.http import parse_accept_header

def rfc7807_response(title: str, code: int=422, type: str='error', **kwargs) -> Response: 
    """
    Create response object based on RFC 7807.

    Supplied **kwargs will be merged into response body
    """
    response = Response()

    if request.accept_mimetypes.accept_json == False:
        response.status_code = 406
        del response.content_type
        return response

    response.status_code = code
    response.mimetype = 'application/problem+json'

    # Field "detail" omitted by design (i18n, deal with that later)
    defaults = {
        'type': 'error',
        'title': title,
        'status': code,
        'instance': request.path
    }

    # Merge defaults with add-on stuff from kwargs
    payload = {**defaults, **kwargs}

    response.data = json.dumps(payload)
    return response
