import smtplib
import os
import smtplib
from dotenv import load_dotenv

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
    smtp_server.sendmail("dr.popov163@gmail.com", "dr.p163@ya.ru", msg.as_string())

    # Закрытие соединения
    smtp_server.quit()

username = "Alex"
text = f"Welcome, {username}!"
title = "Вы прошли верификацию! "
email_sending("dr.p163@ya.ru", text, title)
