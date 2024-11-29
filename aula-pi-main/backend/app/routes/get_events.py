from flask import Blueprint, jsonify, request
from app.guards.auth_required import auth_required
from app.db.connection import get_db

get_events_bp = Blueprint('get_events', __name__)

@get_events_bp.route('/events', methods=['GET'])
@auth_required
def get_events_route(user):
  db = get_db()
  cursor = db.cursor(dictionary=True)

  search = request.args.get('search') or ''

  cursor.execute("""
    SELECT id, title, description, event_date, betting_start_date, betting_end_date, odds_value
    FROM events
    WHERE 
      status = "approved"
      AND (
        title LIKE CONCAT('%', %s, '%')
        OR description LIKE CONCAT('%', %s, '%')
      )
  """, (search, search))

  events = cursor.fetchall()
  cursor.close()

  return jsonify({ "events": events or [] }), 200
