from flask import Blueprint, jsonify
from app.guards.auth_required import auth_required
from app.db.connection import get_db

get_bet_count_bp = Blueprint('get_bet_count', __name__)

@get_bet_count_bp.route('/wallet/bet-count', methods=['GET'])
@auth_required
def get_bet_count_route(user):
  db = get_db()
  cursor = db.cursor()

  user_id = user.get('id')

  cursor.execute("""
    SELECT COUNT(*)
    FROM bets
    WHERE user_id = %s
  """, (user_id,))

  count, = cursor.fetchone()
  cursor.close()

  return jsonify({ "count": count }), 200
