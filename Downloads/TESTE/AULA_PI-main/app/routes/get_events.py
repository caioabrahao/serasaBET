from flask import Blueprint, jsonify
from app.guards.auth_required import auth_required
from app.db.connection import get_db

get_events_bp = Blueprint('get_events', __name__)

@get_events_bp.route('/events', methods=['GET'])
@auth_required
def get_events_route(user):
  db = get_db()
  cursor = db.cursor(dictionary=True)

  cursor.execute("""
    SELECT id, title, description, event_date, betting_start_date, betting_end_date, odds_value
    FROM events
    where status = "approved"
  """)

  events = cursor.fetchall()
  cursor.close()

  return jsonify(events or []), 200
