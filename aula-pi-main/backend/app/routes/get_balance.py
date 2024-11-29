from flask import Blueprint, jsonify
from app.guards.auth_required import auth_required
from app.db.connection import get_db

get_balance_bp = Blueprint('get_balance', __name__)

@get_balance_bp.route('/wallet/balance', methods=['GET'])
@auth_required
def get_balance_route(user):
  db = get_db()
  cursor = db.cursor()

  user_id = user.get('id')

  cursor.execute("""
    SELECT balance
    FROM users
    where id = %s
  """, (user_id,))

  balance, = cursor.fetchone()
  cursor.close()

  return jsonify({ "balance": balance }), 200
