from flask import Blueprint, jsonify
from app.guards.auth_required import auth_required
from app.db.connection import get_db

get_event_bp = Blueprint('get_event', __name__)

@get_event_bp.route('/events/<event_id>', methods=['GET'])
@auth_required
def get_event_route(user, event_id):
  db = get_db()
  cursor = db.cursor(dictionary=True)

  cursor.execute("""
    SELECT id, title, description, event_date, betting_start_date, betting_end_date, odds_value
    FROM events
    where status = "approved" AND id = %s
  """, (event_id,))

  event = cursor.fetchone()
  cursor.close()

  if not event:
    return jsonify({ "message": "Event not found" }), 404

  return jsonify(event), 200
