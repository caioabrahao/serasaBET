from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, validate, ValidationError
from datetime import datetime
import uuid
from app.db.connection import get_db
from app.factories.tokens_factory import tokens_factory
from argon2 import PasswordHasher

register_bp = Blueprint('register', __name__)
ph = PasswordHasher()

class RegisterSchema(Schema):
  name = fields.Str(validate=validate.Length(min=1), required=True)
  date_of_birth = fields.Date(validate=lambda d: d <= datetime.now().date(), required=True)
  email = fields.Email(required=True)
  password = fields.Str(validate=validate.Length(min=8), required=True)

register_schema = RegisterSchema()

@register_bp.route('/register', methods=['POST'])
def register_route():
  json = request.get_json()

  try:
    data = register_schema.load(json)
  except ValidationError as err:
    return jsonify(err.messages), 400
  
  print('hello')
  
  name = data.get('name')
  date_of_birth = data.get('date_of_birth')
  email = data.get('email')
  password = data.get('password')
  
  db = get_db()
  cursor = db.cursor()

  print('connected')

  cursor.execute("""
    SELECT *
    FROM users
    WHERE email = %s
  """, (email,))

  user_with_same_email = cursor.fetchone()
  
  if (user_with_same_email):
    return jsonify({ "message": "Email already in use" }), 409
  
  user_id = str(uuid.uuid4())
  cursor.nextset()

  cursor.execute("""
    INSERT INTO users (id, name, date_of_birth, email, password)
    VALUES (%s, %s, %s, %s, %s);
  """, (user_id, name, date_of_birth, email, ph.hash(password)))

  cursor.close()
  db.commit()

  tokens = tokens_factory({
    "id": user_id,
    "name": name,
    "date_of_birth": date_of_birth,
    "email": email,
  })

  return jsonify(tokens)
