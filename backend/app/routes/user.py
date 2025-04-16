from flask import Blueprint, request, jsonify, current_app
from backend.app.database import db
from backend.app.models.user import User
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

user_bp = Blueprint('user', __name__)

@user_bp.route('/user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        telegram_id = data.get('telegram_id')

        if not telegram_id:
            logger.warning("Telegram ID is missing")
            return jsonify({'error': 'Telegram ID is required'}), 400

        # существует ли пользователь в бд?
        if User.query.filter_by(telegram_id=telegram_id).first():
            logger.info(f"User with telegram_id {telegram_id} already exists")
            return jsonify({'message': 'User already exists'}), 409

        #  есть ли имя в сообщении?
        username = data.get('username')
        if not username:
            logger.info(f"Requesting username for telegram_id {telegram_id}")
            return jsonify({'message': 'Username required'}), 201

        # запрос к Java-серверу
        java_server_url = current_app.config.get('JAVA_SERVER_URL', 'http://jakarta-ee:8080/api/telegram-bot/user') + "/telegram-bot/user"
        java_payload = {
            'telegram_id': telegram_id,
            'username': username
        }
        try:
            java_response = requests.post(
                java_server_url,
                json=java_payload,
                headers={'Content-Type': 'application/json'}
            )

            if java_response.status_code != 200:
                logger.error(f"Java server error: {java_response.status_code}, {java_response.text}")
                return jsonify({'error': 'Failed to register on Java server'}), 500

            java_response_data = java_response.json()
            if not java_response_data.get('success', False): # TODO: а?
                logger.warning(f"Java server rejected registration: {java_response_data}")
                return jsonify({'error': java_response_data.get('message', 'Registration failed')}), 400

        except requests.RequestException as e:
            logger.error(f"Error contacting Java server: {str(e)}")
            return jsonify({'error': 'Failed to contact Java server'}), 500

        # TODO: а если бд питона упадет?
        # регистрируем юзера в бд
        user = User(telegram_id=telegram_id)
        db.session.add(user)
        db.session.commit()

        logger.info(f"User created with telegram_id: {telegram_id}, username: {username}")
        return jsonify({'message': 'User created', 'telegram_id': telegram_id}), 201

    except Exception as e:
        logger.error(f"Error creating user: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
