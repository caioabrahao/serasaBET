from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from datetime import datetime, timezone
import uuid
import pytz
from app.guards.auth_required import auth_required
from app.db.connection import get_db

add_event_bp = Blueprint('add_event', __name__)

class AddEventSchema(Schema):
  title = fields.Str(validate=validate.Length(max=50), required=True)
  description = fields.Str(validate=validate.Length(max=150), required=True)
  odds_value = fields.Decimal(19, validate=lambda qv: qv >= 1, required=True)
  event_date = fields.Date(required=True)
  betting_start_date = fields.AwareDateTime(validate=lambda d: d > datetime.now(pytz.UTC), required=True)
  betting_end_date = fields.AwareDateTime(required=True)

  @validates_schema
  def validate_betting_end_date(self, data, **kwargs):
    if 'betting_start_date' in data and 'betting_end_date' in data:
      if data['betting_end_date'] <= data['betting_start_date']:
        raise ValidationError(
          "betting_end_date must be later than betting_start_date",
          field_name='betting_end_date'
        )
  
  @validates_schema
  def validate_betting_start_date(self, data, **kwargs):
    if 'event_date' in data and 'betting_end_date' in data:
      if data['betting_start_date'] > datetime.combine(
        data['event_date'], 
        datetime.min.time()).replace(tzinfo=timezone.utc
      ):
        raise ValidationError(
          "betting_end_date must be later than betting_start_date",
          field_name='betting_end_date'
        )

add_event_schema = AddEventSchema()

@add_event_bp.route('/events', methods=['POST'])
@auth_required
def add_event_route(user):
  json = request.get_json()

  try:
    data = add_event_schema.load(json)
  except ValidationError as err:
    return jsonify(err.messages), 400
  
  event_id = str(uuid.uuid4())

  title = data.get('title')
  description = data.get('description')
  odds_value = data.get('odds_value')
  event_date = data.get('event_date')
  betting_start_date = data.get('betting_start_date')
  betting_end_date = data.get('betting_end_date')
  
  db = get_db()
  cursor = db.cursor()

  cursor.execute("""
    INSERT INTO events (
      id,
      title,
      description,
      odds_value,
      event_date,
      betting_start_date,
      betting_end_date,
      created_by
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
  """, (
      event_id,
      title, 
      description,
      odds_value,
      event_date,
      betting_start_date,
      betting_end_date,
      user.get('id')
    )
  )

  cursor.close()
  db.commit()

  return { "id": event_id }, 201
