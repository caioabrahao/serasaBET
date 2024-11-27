from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, ValidationError
from enum import Enum
from mysql.connector import Error
from app.guards.auth_required import auth_required
from app.guards.admins_only import admins_only
from app.db.connection import get_db
from app.utils.is_uuid import is_uuid

finish_event_bp = Blueprint('finish_event', __name__)

class EventHappened(Enum):
  yes = "yes"
  no = "no"

class FinishEventSchema(Schema):
  event_happened = fields.Enum(EventHappened, required=True)

finish_event_schema = FinishEventSchema()

@finish_event_bp.route('/events/<event_id>/finish', methods=['PATCH'])
@auth_required
@admins_only
def finish_event_route(user, event_id):
  json = request.get_json()

  if not is_uuid(event_id):
    return jsonify({ "event_id": "Invalid event id" }), 400

  try:
    data = finish_event_schema.load(json)
  except ValidationError as err:
    return jsonify(err.messages), 400

  db = get_db()
  cursor = db.cursor()

  cursor.execute("""
    SELECT *
    FROM events
    WHERE id = %s
  """, (user.get('id'), event_id))

  event = cursor.fetchone()

  if not event:
    return jsonify({ "message": "Event not found" }), 404
  
  event_happened = data.get('event_happened')
  
  cursor.nextset()

  try:
    db.start_transaction()

    cursor.execute("""
      UPDATE events
      SET status = "finished"
      WHERE id = %s
    """, (event_id,))

    cursor.execute("""
      SET @total = (SELECT SUM(amount) FROM bets WHERE event_id = %s);
      SET @right = (SELECT SUM(amount) FROM bets WHERE event_id = %s AND bet = %s);

      UPDATE users u
      JOIN bets b ON u.id = b.user_id
      SET u.balance = u.balance + (b.amount / @right) * @total
      WHERE b.event_id = %s AND b.bet = %s; 
    """, (event_id, event_id, event_happened))
  except Error as err:
    db.rollback()
    raise err

  cursor.close()
  db.commit()

  return '', 204
