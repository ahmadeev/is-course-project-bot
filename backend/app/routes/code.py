from flask import Blueprint, request, jsonify, current_app
from backend.app.database import db
from backend.app.models.session import Session
from backend.app.models.code import Code
from backend.app.models.user import User
from backend.app.tasks.code import send_codes
import threading
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

code_bp = Blueprint('code', __name__)


@code_bp.route('/code/start', methods=['POST'])
def start_code_generation():
    try:
        data = request.get_json()
        telegram_id = data.get('telegram_id')

        if not telegram_id:
            logger.warning("Telegram ID is missing")
            return jsonify({'error': 'Telegram ID is required'}), 400

        user = User.query.filter_by(telegram_id=telegram_id).first()
        if not user:
            logger.warning(f"User with telegram_id {telegram_id} not found")
            return jsonify({'error': 'User not found'}), 404

        session = Session(user_id=user.id)
        db.session.add(session)
        db.session.commit()

        # фоновый поток для отправки кодов
        telegram_token = current_app.config['TELEGRAM_TOKEN']
        thread = threading.Thread(
            target=send_codes,
            args=(current_app._get_current_object(), session.id, telegram_id, telegram_token)
        )
        thread.daemon = True  # завершится при остановке приложения
        thread.start()

        logger.info(f"Started code generation for session {session.id}, telegram_id {telegram_id}")
        return jsonify({'message': 'Code generation started', 'session_id': session.id}), 200

    except Exception as e:
        logger.error(f"Error starting code generation: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500


@code_bp.route('/code/verify', methods=['POST'])
def verify_code():
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        code = data.get('code')

        if not session_id or not code:
            logger.warning("Session ID or code is missing")
            return jsonify({'error': 'Session ID and code are required'}), 400

        session = Session.query.get(session_id)
        if not session or not session.is_active:
            logger.warning(f"Session {session_id} not found or inactive")
            return jsonify({'error': 'Invalid session'}), 404

        code_entry = Code.query.filter_by(session_id=session_id, code=code, is_used=False, is_expired=False).first()
        if not code_entry:
            logger.warning(f"Invalid or expired code {code} for session {session_id}")
            return jsonify({'error': 'Invalid or expired code'}), 400

        code_entry.is_used = True
        Code.query.filter_by(session_id=session_id).update({'is_expired': True})
        session.is_active = False
        db.session.commit()

        logger.info(f"Code {code} verified for session {session_id}")
        return jsonify({'message': 'Code verified'}), 200

    except Exception as e:
        logger.error(f"Error verifying code: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500