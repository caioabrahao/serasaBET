from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db import Base


DATABASE_URL = "mysql+mysqlconnector://root:1234@localhost:3306/Klar"
engine = create_engine(DATABASE_URL)

# Cria a sessão do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria a classe base para os modelos
Base = declarative_base()

# Modelo do Usuário
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    birthdate = Column(Date, nullable=False)
    balance = Column(Float, default=0.0)  # Saldo do usuário

    bets = relationship("Bet", back_populates="user")


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(String(500), nullable=True)
    category = Column(String(255), nullable=False)
    status = Column(String(50), default='pending')
    approved = Column(Boolean, default=False)  # Adicione esta linha
    created_by = Column(Integer, ForeignKey('users.id'))

    creator = relationship("User")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date.strftime("%Y-%m-%d"),
            "description": self.description,
            "category": self.category,
            "status": self.status,
            "approved": self.approved,  # Adicione esta linha se quiser retornar também
            "created_by": self.created_by,
        }
    
# Modelo da Aposta
class Bet(Base):
    __tablename__ = 'bets'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # usuário que fez a aposta
    event_id = Column(Integer, ForeignKey('events.id'))  # evento que foi apostado
    amount = Column(Float, nullable=False)  # Valor da aposta
    outcome = Column(String(50), nullable=True)  # Resultado da aposta

    user = relationship("User", back_populates="bets") 
    event = relationship("Event") 

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)