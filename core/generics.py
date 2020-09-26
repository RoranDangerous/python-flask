import json
from sqlalchemy import exc
from flask import request, make_response, jsonify
from flask_restful import Api as FlaskApi, Resource as FlaskResource, reqparse, abort
from flask_jwt_extended import verify_jwt_in_request
from core import db

class Resource(FlaskResource):
  authentication_required = True
  model = None
  apply_filters = []

  def __init__(self, *args, **kwargs):
    '''
    Custom __init__ to:
      - Check if user authenticated
      - Check for required fields
    '''

    if self.authentication_required:
      verify_jwt_in_request()

    super(Resource, self).__init__(*args, **kwargs)

    self.request = request

    self.parser = reqparse.RequestParser()
    try:
      required_fields = getattr(self, 'required_fields')
    except AttributeError:
      required_fields = []

    for field in required_fields:
      self.parser.add_argument(field, help='This filed cannot be blank', required=True)

    try:
      json_data = json.loads(request.data, strict=False)
    except json.JSONDecodeError as ex:
      json_data = {}

    self.data = { **self.parser.parse_args(), **json_data }

  def get_query(self):
    assert self.model, '"model" field is invalid.'

    query = self.model.query

    for query_filter in self.apply_filters:
      query = query.filter(query_filter.as_filter(request=request))

    return query


class SingleResource(Resource):
  editable_fields = []

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    assert self.model, '"model" field is invalid.'

  def get_object(self, id):
    obj = self.get_query().filter(self.model.id == id).first()

    return obj or abort(make_response(jsonify({'message': 'Resource not found'}), 404))

  def get(self, id):
    return self.get_object(id).serialize

  def delete(self, id):
    obj = self.get_object(id)

    db.session.delete(obj)
    db.session.commit()

    return {'success': True}

  def patch(self, id):
    obj = self.get_object(id)

    [
      setattr(obj, edit_field, self.data.get(edit_field))
      for edit_field in self.editable_fields
      if edit_field in self.data
    ]

    db.session.commit()

    return obj.serialize


class ListResource(Resource):
  def get(self):
    return [m.serialize for m in self.get_query().all()]