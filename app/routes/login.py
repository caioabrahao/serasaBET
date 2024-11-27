from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, validate, ValidationError
from app.db.connection import get_db
from app.factories.tokens_factory import tokens_factory
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

login_bp = Blueprint('login', __name__)
ph = PasswordHasher()

class LoginSchema(Schema):
  email = fields.Email(required=True)
  password = fields.Str(validate=validate.Length(min=8), required=True)

login_schema = LoginSchema()

@login_bp.route('/login', methods=['POST'])
def login_route():
  json = request.get_json()

  try:
    data = login_schema.load(json)
  except ValidationError as err:
    return jsonify(err.messages), 400
  
  email = data.get('email')
  password = data.get('password')
  
  db = get_db()
  cursor = db.cursor(dictionary=True)

  cursor.execute("""
    SELECT id, password, role
    FROM users
    WHERE email = %s
  """, (email,))
  
  user = cursor.fetchone()
  
  if (not user):
    return jsonify({ "message": "Incorrect email or password" }), 401
  
  try:
    hashed_password = user.get('password')
    ph.verify(hashed_password, password)
  except VerifyMismatchError:
    return jsonify({ "message": "Incorrect email or password" }), 401

  tokens = tokens_factory({
    "id": user.get('id'),
    "email": email,
    "role": user.get('role'),
  })

  return jsonify(tokens)
