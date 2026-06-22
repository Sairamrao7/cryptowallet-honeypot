from . import db
from datetime import datetime

class WalletImport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip = db.Column(db.String(32))
    user_agent = db.Column(db.String(256))
    wallet_type = db.Column(db.String(32))
    credential_hash = db.Column(db.String(128))

class SendAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip = db.Column(db.String(32))
    user_agent = db.Column(db.String(256))
    to_address = db.Column(db.String(128))
    amount = db.Column(db.Float)
    credential_hash = db.Column(db.String(128))

class BehaviorLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip = db.Column(db.String(32))
    user_agent = db.Column(db.String(256))
    typing_speed = db.Column(db.Float)
    mouse_movements = db.Column(db.Text)
    session_id = db.Column(db.String(64))