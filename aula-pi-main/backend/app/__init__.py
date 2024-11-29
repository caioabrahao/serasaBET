from flask import Flask
from dotenv import load_dotenv
from flask_cors import CORS
from app.routes.register import register_bp
from app.routes.login import login_bp
from app.routes.refresh_session import refresh_session_bp
from app.routes.add_event import add_event_bp
from app.routes.get_events_overview import get_events_overview_bp
from app.routes.get_events import get_events_bp
from app.routes.get_event import get_event_bp
from app.routes.evaluate_event import evaluate_event_bp
from app.routes.revoke_event import revoke_event_bp
from app.routes.deposit_into_wallet import deposit_into_wallet_bp
from app.routes.withdraw_from_wallet import withdraw_from_wallet_bp
from app.routes.get_bet_count import get_bet_count_bp
from app.routes.get_balance import get_balance_bp
from app.routes.get_wallet_history import get_wallet_history_bp
from app.routes.bet_on_event import bet_on_event_bp
from app.routes.finish_event import finish_event_bp

load_dotenv()

def create_app():
  app = Flask(__name__)
  CORS(app, supports_credentials=True)

  app.config.from_object('config')

  app.register_blueprint(register_bp)
  app.register_blueprint(login_bp)
  app.register_blueprint(add_event_bp)
  app.register_blueprint(get_events_overview_bp)
  app.register_blueprint(get_events_bp)
  app.register_blueprint(get_event_bp)
  app.register_blueprint(evaluate_event_bp)
  app.register_blueprint(revoke_event_bp)
  app.register_blueprint(deposit_into_wallet_bp)
  app.register_blueprint(withdraw_from_wallet_bp)
  app.register_blueprint(get_bet_count_bp)
  app.register_blueprint(get_balance_bp)
  app.register_blueprint(get_wallet_history_bp)
  app.register_blueprint(bet_on_event_bp)
  app.register_blueprint(finish_event_bp)
  app.register_blueprint(refresh_session_bp)

  return app