from flask import request, jsonify
from functools import wraps
import jwt
import os

def auth_required(f):
  @wraps(f)
  def wrapper(*args, **kwargs):
    access_token = request.cookies.get('access_token')

    try:
      user = jwt.decode(access_token, os.environ.get('JWT_SECRET'), algorithms=["HS256"])
    except Exception:
      return jsonify({ "message": "Unauthorized" }), 401
    
    user['id'] = user.pop('sub')
    return f(user, *args, **kwargs)

  return wrapper
