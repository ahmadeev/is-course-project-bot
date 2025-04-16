import random
import string
import threading
import time
import requests
from backend.app.database import db
from backend.app.models.session import Session
from backend.app.models.code import Code
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def send_codes(app, session_id, telegram_id, telegram_token):
    telegram_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"

    while True:
        with app.app_context():
            session = Session.query.get(session_id)
            if not session or not session.is_active:
                logger.info(f"Session {session_id} stopped")
                break

            code = generate_code()
            code_entry = Code(session_id=session_id, code=code)
            db.session.add(code_entry)
            db.session.commit()

            try:
                response = requests.post(telegram_url, json={
                    'chat_id': telegram_id,
                    'text': f"Your verification code: {code}"
                })
                if response.status_code == 200:
                    logger.info(f"Sent code {code} to telegram_id {telegram_id}")
                else:
                    logger.error(f"Failed to send code to telegram_id {telegram_id}: {response.text}")
            except Exception as e:
                logger.error(f"Failed to send code to telegram_id {telegram_id}: {str(e)}")

        time.sleep(10)
