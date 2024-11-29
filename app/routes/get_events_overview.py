from flask import Blueprint, jsonify
from app.guards.auth_required import auth_required
from app.db.connection import get_db

get_events_overview_bp = Blueprint('get_events_overview', __name__)

@get_events_overview_bp.route('/events/overview', methods=['GET'])
@auth_required
def get_events_overview_route(user):
  db = get_db()
  cursor = db.cursor(dictionary=True)

  cursor.execute("""
    SELECT 
      e.id, 
      e.title,
      e.description,
      e.odds_value,
      COUNT(b.id) AS bet_count
    FROM 
      events e
    LEFT JOIN 
      bets b ON e.id = b.event_id
    WHERE
      e.status = "approved"
    GROUP BY 
      e.id
    ORDER BY 
      bet_count DESC
    LIMIT 8        
  """)

  most_bet_events = cursor.fetchall()

  cursor.nextset()

  cursor.execute("""
    SELECT 
      e.id,
      e.title,
      e.description,
      e.odds_value,
      COUNT(b.id) AS bet_count  
    FROM 
      events e
    LEFT JOIN 
      bets b ON e.id = b.event_id
    WHERE 
      e.status = "approved" AND e.betting_end_date <= NOW() + INTERVAL 48 HOUR
    GROUP BY 
      e.id
    ORDER BY 
      e.betting_end_date ASC
    LIMIT 8
  """)

  events_closing_soon = cursor.fetchall()
  cursor.close()

  return jsonify({ 
    "events_closing_soon": events_closing_soon,
    "most_bet_events": most_bet_events 
  }), 200
