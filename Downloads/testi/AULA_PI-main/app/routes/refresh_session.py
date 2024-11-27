from flask import Blueprint, jsonify, request
from jwt.exceptions import DecodeError
import jwt
import os
from app.db.connection import get_db
from app.factories.tokens_factory import tokens_factory

refresh_session_bp = Blueprint('refresh_session', __name__)

@refresh_session_bp.route('/refresh-session', methods=['POST'])
def refresh_session_route():
  refresh_token = request.cookies.get('refresh-token')

  try:
    token = jwt.decode(refresh_token, os.environ.get('JWT_SECRET'))
    user_id = token.get('sub')
  except DecodeError:
    return jsonify({ "message": "Unauthorized" }), 401

  db = get_db()
  cursor = db.cursor()

  cursor.execute("""
    SELECT email, role
    FROM users
    WHERE id = %s
  """, (user_id,))  

  email, role = cursor.fetchone()

  tokens = tokens_factory({
    "id": user_id,
    "email": email,
    "role": role,
  })

  return jsonify(tokens)


