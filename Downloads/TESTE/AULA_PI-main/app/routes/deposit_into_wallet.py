from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, ValidationError
import uuid
from app.guards.auth_required import auth_required
from app.db.connection import get_db

deposit_into_wallet_bp = Blueprint('deposit_into_wallet', __name__)

class DepositIntoWalletSchema(Schema):
  amount = fields.Decimal(19, validate=lambda a: a > 0, required=True)

deposit_into_wallet_schema = DepositIntoWalletSchema()

@deposit_into_wallet_bp.route('/wallet/deposit', methods=['POST'])
@auth_required
def deposit_into_wallet_route(user):
  json = request.get_json()

  try:
    data = deposit_into_wallet_schema.load(json)
  except ValidationError as err:
    return jsonify(err.messages), 400
  
  user_id = user.get('id')
  amount = data.get('amount')

  db = get_db()
  cursor = db.cursor()

  cursor.execute("""
    UPDATE users
    SET balance = balance + %s
    WHERE id = %s
  """, (amount, user_id))

  cursor.nextset()
  transaction_id = str(uuid.uuid4())

  cursor.execute("""
    INSERT INTO transactions (id, type, user_id, amount)
    VALUES (%s, 'deposit', %s, %s)
  """, (transaction_id, user_id, amount))

  cursor.close()
  db.commit()

  return '', 204
