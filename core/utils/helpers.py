from flask import make_response, jsonify
from flask_restful import abort

def get_or_404(model, *expressions, message=""):
    obj = model.query.filter(*expressions).first()

    return obj or abort(make_response(jsonify({'message': message or 'Resource not found'}), 404))