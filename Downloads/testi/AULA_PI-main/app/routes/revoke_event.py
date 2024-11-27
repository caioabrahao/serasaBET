from flask import Blueprint, jsonify
from app.guards.auth_required import auth_required
from app.db.connection import get_db
from app.utils.is_uuid import is_uuid

revoke_event_bp = Blueprint('revoke_event', __name__)

@revoke_event_bp.route('/events/<event_id>/revoke', methods=['PATCH'])
@auth_required
def revoke_event_route(user, event_id):
  if not is_uuid(event_id):
    return jsonify({ "event_id": "Invalid event id" }), 400

  db = get_db()
  cursor = db.cursor(dictionary=True)

  cursor.execute("""
    SELECT *
    FROM events
    WHERE created_by = %s AND id = %s
  """, (user.get('id'), event_id))

  event = cursor.fetchone()

  if not event:
    return jsonify({ "message": "Event not found" }), 404
  
  cursor.nextset()

  cursor.execute("""
    SELECT *
    FROM bets
    WHERE event_id = %s
  """, (event_id,))

  bet = cursor.fetchone()

  if bet:
    return jsonify({ "message": "Cannot revoke events with bets." })
  
  cursor.nextset()

  cursor.execute("""
    UPDATE events
    SET status = "revoked", disapproval_reason = NULL
    WHERE id = %s
  """, (event_id,))

  cursor.close()
  db.commit()

  return '', 204
