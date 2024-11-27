from flask import jsonify
from functools import wraps

def admins_only(f):
  @wraps(f)
  def wrapper(user, *args, **kwargs):
    if user.get('role') != 'admin':
      return jsonify({ "message": "You don't have permission to do this" })

    return f(user, *args, **kwargs)

  return wrapper
