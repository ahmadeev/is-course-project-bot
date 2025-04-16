from backend.app.database import db
from datetime import datetime


class Code(db.Model):
    __tablename__ = 'codes'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    code = db.Column(db.String(6), nullable=False)
    is_used = db.Column(db.Boolean, default=False)
    is_expired = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    session = db.relationship('Session', backref='codes')
    