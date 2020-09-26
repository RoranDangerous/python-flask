from flask_restful import Api
from flask import Blueprint
from core import app
from core.auth import resources

blueprint = Blueprint('auth', __name__)
api = Api(blueprint)
app.register_blueprint(blueprint, url_prefix='/api/auth')

# URLs
api.add_resource(resources.Registration, '/register', strict_slashes=False)
api.add_resource(resources.Login, '/login', strict_slashes=False)
api.add_resource(resources.VerifyToken, '/token/verify', strict_slashes=False)
api.add_resource(resources.Secret, '/secret', strict_slashes=False)
api.add_resource(resources.PusherAuth, '/pusher', strict_slashes=False)