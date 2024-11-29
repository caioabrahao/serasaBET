from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, ValidationError
from mysql.connector import Error
from app.guards.auth_required import auth_required
from app.db.connection import get_db
from app.utils.is_uuid import is_uuid
from enum import Enum
import uuid
from datetime import datetime
from decimal import Decimal

bet_on_event_bp = Blueprint('bet_on_event', __name__)

class Bet(Enum):
  yes = 'yes',
  no = 'no'

class BetOnEventSchema(Schema):
  bet = fields.Enum(Bet, required=True)
  amount = fields.Decimal(19, validate=lambda a: a >= 1, required=True)

bet_on_event_schema = BetOnEventSchema()

@bet_on_event_bp.route('/events/<event_id>/bets', methods=['POST'])
@auth_required
def bet_on_event_route(user, event_id):
  if not is_uuid(event_id):
    return jsonify({ "event_id": "Invalid event id" }), 400
  
  json = request.get_json()

  try:
    data = bet_on_event_schema.load(json)
  except ValidationError as err:
    return jsonify(err.messages), 400
  
  bet = data.get('bet')
  amount = data.get('amount')

  db = get_db()
  cursor = db.cursor()

  cursor.execute("""
    SELECT betting_start_date, betting_end_date
    FROM events
    WHERE status = "approved" AND id = %s
  """, (event_id,))

  event = cursor.fetchone()

  if not event:
    return jsonify({ "message": "Event not found" }), 404
  
  betting_start_date, betting_end_date = event
  now = datetime.now()

  if now < betting_start_date or now >= betting_end_date:
    return jsonify({ "message": "This event is currently not accepting bets" }), 422
  
  cursor.nextset()
  user_id = user.get('id')

  cursor.execute("""
    SELECT balance
    FROM users
    WHERE id = %s
  """, (user_id,))

  balance, = cursor.fetchone()

  if amount > Decimal(balance):
    return jsonify({ "message": "Insufficient balance" }), 422

  cursor.nextset()
  bet_id = str(uuid.uuid4())

  try:
    db.start_transaction()

    cursor.execute("""
      UPDATE users
      SET balance = balance - %s,
      WHERE id = %s
    """, (amount, user_id))

    cursor.execute("""
      INSERT INTO bets (id, user_id, event_id, bet, amount)
      VALUES (%s, %s, %s, %s, %s)
    """, (bet_id, user_id, event_id, bet, amount))
  except Error as err:
    db.rollback()
    raise err

  cursor.close()
  db.commit()

  return '', 204
