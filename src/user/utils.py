import jwt
from fastapi import HTTPException, status
from email_validator import validate_email, EmailNotValidError
import smtplib
import os
import smtplib
from dotenv import load_dotenv

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

secret_key = "ijasfdioj83rj89jafsd83jaf8"
algorithm = "HS256"

def check(email: str):
    try:
        v = validate_email(email) 
        return True
    except EmailNotValidError as e:
        return False


def make_token(user_id: int) -> str:
    payload = {
        "user_id": user_id,
    }
    token = jwt.encode(payload, secret_key, algorithm)
    return token


def valid_and_decode_token(token: str) -> int:  # в токене зашит user_id
    try:
        payload = jwt.decode(token, secret_key, [algorithm])
        print(type(payload), payload)
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Срок действия токена истек"
        ) from None
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Отказано в доступе"
        ) from None

def email_sending(email: str, text: str, title: str):
    load_dotenv()

    popov163 = os.getenv('popov163')

    smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_server.starttls()
    smtp_server.login("dr.popov163@gmail.com", popov163)


    # Создание объекта сообщения
    msg = MIMEMultipart()

    # Настройка параметров сообщения
    msg["From"] = "dr.popov163@gmail.com"
    msg["To"] = email
    msg["Subject"] = title

    # Добавление текста в сообщение
    msg.attach(MIMEText(text, "plain"))

    # Отправка письма
    smtp_server.sendmail("dr.popov163@gmail.com", email, msg.as_string())

    # Закрытие соединения
    smtp_server.quit()


