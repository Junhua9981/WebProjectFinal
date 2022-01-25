
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from fastapi_mail.email_utils import DefaultChecker
from decouple import config

conf = ConnectionConfig(
    MAIL_USERNAME = config('MAIL_USERNAME'),
    MAIL_PASSWORD = config('MAIL_PASSWORD'),
    MAIL_FROM = config('MAIL_FROM'),
    MAIL_PORT = config('MAIL_PORT'),
    MAIL_SERVER = config('MAIL_SERVER'),
    MAIL_FROM_NAME=config('MAIL_FROM_NAME'),
    MAIL_TLS = True,
    MAIL_SSL = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_mail(email_to: str, subject: str, randomTk: str):
    mail = FastMail(conf)
    msg = MessageSchema(
        recipients=[email_to],
        subject="Activate your account",
        body="這是您的帳號驗證碼:"+randomTk,
        subtype="html"
    )
    await mail.send_message(msg)