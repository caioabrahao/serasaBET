from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, ValidationError
import uuid
from datetime import datetime
from app.guards.auth_required import auth_required
from app.db.connection import get_db

withdraw_from_wallet_bp = Blueprint('withdraw_from_wallet', __name__)

class WithdrawFromWalletSchema(Schema):
  amount = fields.Decimal(19, validate=lambda a: a > 0, required=True)

withdraw_from_wallet_schema = WithdrawFromWalletSchema()
DAILY_WITHDRAWAL_LIMIT = 101_000

@withdraw_from_wallet_bp.route('/wallet/withdraw', methods=['POST'])
@auth_required
def withdraw_from_wallet_route(user):
  json = request.get_json()

  try:
    data = withdraw_from_wallet_schema.load(json)
  except ValidationError as err:
    return jsonify(err.messages), 400
  
  user_id = user.get('id')
  amount = data.get('amount')

  db = get_db()
  cursor = db.cursor()

  cursor.execute("""
    SELECT balance
    FROM users
    WHERE id = %s
  """, (user_id,))

  balance, = cursor.fetchone()

  if amount > balance:
    return jsonify({ "message": "Insufficient balance" }), 422
  
  now = datetime.now().date()
  today = now.strftime('%Y-%m-%d')

  cursor.nextset()

  # dates are not compared correctly
  cursor.execute("""
    SELECT COALESCE(SUM(amount), 0)
    FROM transactions
    WHERE user_id = %s AND DATE(created_at) = %s AND type = 'withdraw'
  """, (user_id, today))

  amount_withdrawn_today, = cursor.fetchone()

  if amount_withdrawn_today + amount > DAILY_WITHDRAWAL_LIMIT:
    return jsonify({ "message": "Reached the daily withdrawal limit" }), 422

  cursor.nextset()

  cursor.execute("""
    UPDATE users
    SET balance = balance - %s
    WHERE id = %s
  """, (amount, user_id))

  cursor.nextset()
  transaction_id = str(uuid.uuid4())

  cursor.execute("""
    INSERT INTO transactions (id, type, user_id, amount)
    VALUES (%s, 'withdraw', %s, %s)
  """, (transaction_id, user_id, amount))

  cursor.close()
  db.commit()

  return '', 204
