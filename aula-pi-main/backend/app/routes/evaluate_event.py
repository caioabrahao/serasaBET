from flask import Blueprint, jsonify, request
from marshmallow import Schema, fields, ValidationError, validates_schema
from enum import Enum
from app.guards.auth_required import auth_required
from app.guards.admins_only import admins_only
from app.db.connection import get_db
from app.utils.is_uuid import is_uuid
import resend
import os

evaluate_event_bp = Blueprint('evaluate_event', __name__)
resend.api_key = os.environ["RESEND_API_KEY"]

class EventEvaluationStatus(Enum):
  approved = "approved"
  disapproved = "disapproved"

class EvaluateEventSchema(Schema):
  status = fields.Enum(EventEvaluationStatus, required=True)
  disapproval_reason = fields.Str()

  @validates_schema
  def validate(self, data, **kwargs):
    if 'status' in data and 'disapproval_reason' not in data:
      if data['status'] == EventEvaluationStatus.disapproved:
        raise ValidationError(
          "disapproval_reason is required when status is disapproved.", 
          field_names=["disapproval_reason"]
       )

evaluate_event_schema = EvaluateEventSchema()

@evaluate_event_bp.route('/events/<event_id>/evaluate', methods=['PATCH'])
@auth_required
@admins_only
def evaluate_event_route(user, event_id):
  json = request.get_json()

  if not is_uuid(event_id):
    return jsonify({ "event_id": "Invalid event id" }), 400

  try:
    data = evaluate_event_schema.load(json)
  except ValidationError as err:
    return jsonify(err.messages), 400

  db = get_db()
  cursor = db.cursor(dictionary=True)

  cursor.execute("""
    SELECT title, created_by
    FROM events
    WHERE id = %s
  """, (event_id,))

  event = cursor.fetchone()

  cursor.nextset()

  cursor.execute("""
    SELECT email
    FROM users
    WHERE id = %s
  """, (event.get('created_by'),))

  creator = cursor.fetchone()

  if not event:
    return jsonify({ "message": "Event not found" }), 404
  
  status = data.get('status')
  disapproval_reason = data.get('disapproval_reason')
  
  cursor.nextset()

  if status == EventEvaluationStatus.approved:
    cursor.execute("""
      UPDATE events
      SET status = "approved"
      WHERE id = %s
    """, (event_id,))
  else:
    cursor.execute("""
      UPDATE events
      SET status = "disapproved", disapproval_reason = %s
      WHERE id = %s
    """, (disapproval_reason, event_id))

    resend_params: resend.Emails.SendParams = {
      "from": "SerasaBet <serasabet@spents.tech>",
      "to": [creator.get('email')],
      "subject": f"{event.get('title')} was disapproved.",
      "html": f"Hi! Your event {event.get('title')} was disapproved due to {disapproval_reason}.",
    }

    resend.Emails.send(resend_params)

  cursor.close()
  db.commit()

  return '', 204
