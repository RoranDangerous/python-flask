from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity
from jwt import ExpiredSignatureError, DecodeError
from flask import request
from core import db, bcrypt, pusher
from core.utils import channels
from core.generics import Resource
from core.auth.models import User


class Registration(Resource):
  authentication_required = False
  required_fields = ['email', 'password']

  def post(self):
    user = User.query.filter_by(email=self.data.get('email')).first()
    if user:
      return {'message': 'User with this email already exists.'}, 400

    user = User(
        email=self.data.get('email'),
        password=self.data.get('password')
    )
    db.session.add(user)
    db.session.commit()
    return {
      'user': {
        'email': user.email
      },
      'token': user.token
    }


class Login(Resource):
  authentication_required = False
  required_fields = ['email', 'password']

  def post(self):
    user = User.query.filter_by(email=self.data.get('email')).first()
    if user and bcrypt.check_password_hash(user.password, self.data.get('password')):
      return {
        'user': {
          'email': user.email
        },
        'token': user.token
      }
    else:
      return {'message': 'Please enter correct email and password.'}, 400


class VerifyToken(Resource):
  authentication_required = False

  def get(self):
    try:
      verify_jwt_in_request()

      user = get_jwt_identity()
      return {
        'success': True,
        'user': user
      }
    except ExpiredSignatureError:
      return {
        'message': 'Token expired',
        'expired': True
      }
    except DecodeError as ex:
      print(f'[Verify Token] Error decoding token: {ex.__class__.__name__}({ex})')
      return {
        'message': 'Decoding error',
        'success': False
      }
    except Exception as ex:
      print(f'[Verify Token] Unexpected exception: {ex.__class__.__name__}({ex})')
      return {
        'message': 'Unknown error',
        'success': False
      }


class Secret(Resource):
  def get(self):
    return {'answer': 42}


class PusherAuth(Resource):
  def post(self):
    user = get_jwt_identity()
    channel_name = request.form['channel_name']
    channel = channels.get_channel_from_name(channel_name)

    if not channel or not channel.is_authorized(user.get('id')):
      return {'message': 'Unauthorized'}, 403

    return pusher.authenticate(
      channel=channel_name,
      socket_id=request.form['socket_id']
    )