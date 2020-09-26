import datetime
from flask_jwt_extended import create_access_token
from core import app, db, bcrypt, jwt


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

        self.password = bcrypt.generate_password_hash(
            kwargs.get('password'), app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.registered_on = datetime.datetime.now()

    @property
    def token(self):
        return create_access_token(identity=self)


@jwt.user_identity_loader
def user_identity_lookup(user):
    ''' Custom data that is returned on get_jwt_identity() '''
    return {
        'id': user.id,
        'email': user.email
    }


class BlacklistToken(db.Model):
    """ Token Model for storing JWT tokens """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return "<id: token: {}".format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False