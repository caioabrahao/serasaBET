from flask import Blueprint, jsonify
from app.guards.auth_required import auth_required
from app.db.connection import get_db

get_wallet_history_bp = Blueprint('get_wallet_history', __name__)

@get_wallet_history_bp.route('/wallet/history', methods=['GET'])
@auth_required
def get_wallet_history_route(user):
  db = get_db()
  cursor = db.cursor(dictionary=True)

  user_id = user.get('id')

  cursor.execute("""
    SELECT id, 'deposit' AS type, amount, created_at
    FROM transactions
    WHERE user_id = %s AND type = 'deposit'

    UNION ALL

    SELECT id, 'bet' AS type, amount, created_at
    FROM bets
    WHERE user_id = %s

    ORDER BY created_at;
  """, (user_id, user_id))

  history = cursor.fetchall()
  print(history)
  cursor.close()

  return jsonify(history or []), 200
