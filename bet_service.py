from flask import request, jsonify
from db import SessionLocal
from models import Bet, User, Event

def add_funds():
    data = request.get_json()
    email = data.get('email')
    amount = data.get('amount')

    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    
    if user:
        user.balance += amount
        db.commit()
        db.close()
        return jsonify({"message": "Fundos adicionados com sucesso."})

    return jsonify({"message": "Usuário não encontrado."}), 404

def withdraw_funds():
    data = request.get_json()
    email = data.get('email')
    amount = data.get('amount')

    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()

    if user and user.balance >= amount:
        user.balance -= amount
        db.commit()
        db.close()
        return jsonify({"message": "Saque realizado com sucesso."})
    
    return jsonify({"message": "Saldo insuficiente ou usuário não encontrado."}), 400

def bet_on_event():
    data = request.get_json()
    email = data.get('email')
    event_id = data.get('event_id')
    amount = data.get('amount')

    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    event = db.query(Event).filter(Event.id == event_id).first()

    if user and event and user.balance >= amount and event.approved:
        user.balance -= amount
        bet = Bet(user_id=user.id, event_id=event_id, amount=amount)
        db.add(bet)
        db.commit()
        db.close()
        return jsonify({"message": "Aposta realizada com sucesso."})

    return jsonify({"message": "Erro ao realizar a aposta."}), 400

def finish_event(event_id):
    data = request.get_json()
    outcome = data.get('outcome')  # True para vitória, False para derrota

    db = SessionLocal()
    event = db.query(Event).filter(Event.id == event_id).first()

    if event:
        bets = db.query(Bet).filter(Bet.event_id == event_id).all()
        for bet in bets:
            if outcome:
                bet.won = True
                user = db.query(User).filter(User.id == bet.user_id).first()
                user.balance += bet.amount * 2  # Multiplica o valor da aposta em caso de vitória

        db.commit()
        db.close()
        return jsonify({"message": "Evento finalizado e apostas processadas."})

    return jsonify({"message": "Evento não encontrado."}), 404

def search_event():
    keyword = request.args.get('keyword')

    db = SessionLocal()
    events = db.query(Event).filter(Event.name.like(f'%{keyword}%')).all()
    db.close()

    return jsonify([{
        'id': event.id,
        'name': event.name,
        'date': event.date
    } for event in events])
