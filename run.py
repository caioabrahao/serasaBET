from flask import Flask, request, jsonify
from db import SessionLocal, engine
from models import Event
from auth_service import sign_up, login
from event_service import add_event, get_events, delete_event, evaluate_event
from bet_service import add_funds, withdraw_funds, bet_on_event, finish_event, search_event

app = Flask(__name__)


@app.route('/')
def home():
    return jsonify({"message": "Bem-vindo ao sistema de apostas!"})

# Rotas de autenticação
@app.route('/signUp', methods=['POST'])
def register_user():
    return sign_up()

@app.route('/login', methods=['POST'])
def login_user():
    return login()

# Rotas de eventos
@app.route('/addNewEvent', methods=['POST'])
def add_event_route():
    data = request.json
    name = data.get('name')
    date = data.get('date')
    description = data.get('description')
    category = data.get('category')
    created_by = data.get('created_by')


    if not all([name, date, description, category, created_by]):
        return jsonify({"message": "All fields are required"}), 400

    with SessionLocal() as db:
        try:
            event = add_event(db, name, date, description, category, created_by)
            return jsonify({"message": "Event added successfully", "event": event.to_dict()}), 201
        except Exception as e:
            db.rollback()
            return jsonify({"message": "Error adding event", "error": str(e)}), 500

@app.route('/get_events', methods=['GET'])
def get_events_route():
    with SessionLocal() as db:
        events = db.query(Event).all()  
        return jsonify([event.to_dict() for event in events]), 200  # json
@app.route('/deleteEvent/<int:event_id>', methods=['DELETE'])
def remove_event(event_id):
    return delete_event(event_id)

@app.route('/evaluateEvent', methods=['POST'])
def evaluate_event_route():
    data = request.json
    event_id = data.get('event_id')
    approve = data.get('approve')


    if event_id is None or approve is None:
        return jsonify({"message": "Event ID and approval decision are required"}), 400

    with SessionLocal() as db:
        try:

            approve = bool(approve)


            event = evaluate_event(db, event_id, approve)

            if isinstance(event, dict):
                return jsonify(event), event.get("status_code", 400)

            return jsonify({"message": "Event evaluated successfully", "event": event.to_dict()}), 200
        except Exception as e:
            db.rollback()
            return jsonify({"message": "Error evaluating event", "error": str(e)}), 500

    
# Rotas de apostas
@app.route('/addFunds', methods=['POST'])
def add_user_funds():
    return add_funds()

@app.route('/withdrawFunds', methods=['POST'])
def withdraw_user_funds():
    return withdraw_funds()

@app.route('/betOnEvent', methods=['POST'])
def make_bet():
    return bet_on_event()

@app.route('/finishEvent/<int:event_id>', methods=['POST'])
def conclude_event(event_id):
    return finish_event(event_id)

@app.route('/searchEvent', methods=['GET'])
def search_for_event():
    return search_event()

if __name__ == '__main__':
    app.run(debug=True)
