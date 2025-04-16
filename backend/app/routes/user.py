from flask import Blueprint, request, jsonify
from backend.app.database import db
from backend.app.models.user import User

user_bp = Blueprint('user', __name__)


@user_bp.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    telegram_id = data.get('telegram_id')

    if not telegram_id:
        return jsonify({'error': 'Telegram ID is required'}), 400

    if User.query.filter_by(telegram_id=telegram_id).first():
        return jsonify({'message': 'User already exists'}), 409

    user = User(telegram_id=telegram_id)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created', 'telegram_id': telegram_id}), 201
