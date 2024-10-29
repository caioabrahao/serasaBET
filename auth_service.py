from flask import request, jsonify
from db import SessionLocal
from models import User
import jwt
import datetime

def sign_up():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']  # Sem hash
    birthdate = data['birthdate']
    
    new_user = User(name=name, email=email, password=password, birthdate=birthdate)
    
    db = SessionLocal()
    db.add(new_user)
    db.commit()
    db.close()
    
    return jsonify({"message": "Usuário cadastrado com sucesso!"})

def login():
    data = request.get_json()
    email = data['email']
    password = data['password']  # Senha usuário
    
    db = SessionLocal()
    user = db.query(User).filter(User.email == email).first()
    
    if user and user.password == password:  # Comparação direta
        return jsonify({"message": "Login realizado com sucesso"})
    else:
        return jsonify({"message": "Email ou senha incorretos"}), 401