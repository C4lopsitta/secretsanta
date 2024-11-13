import ssl
from os import getenv

from fastapi.templating import Jinja2Templates
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import smtplib


templates = Jinja2Templates(directory="templates")

_internal_email = getenv("EMAIL")
_email_auth_paswd = getenv("EMAIL_PASSWORD")
_email_server = getenv("EMAIL_SERVER")
_email_context = ssl.create_default_context()


def get_gift_mail(sender_name: str,
                  receiver_name: str,
                  admin_email: str) -> str:
    return templates.get_template(name="emails/gift.html").render(context={
        "id": "",
        "sender_name": sender_name,
        "gift_receiver": receiver_name,
        "admin_email": admin_email,
    })


def send_gift_mail(gift_sender_name: str,
                   gift_sender_email: str,
                   gift_reciver_name: str,
                   admin_email: str):
    mail_mesg = MIMEMultipart("alternative")
    mail_mesg["Subject"] = "Secret Santa"
    mail_mesg["From"] = _internal_email
    mail_mesg["To"] = gift_sender_email

    mail_plaintext = f"""
{gift_sender_name}, dovrai fare il tuo regalo a {gift_reciver_name}!
"""
    mail_html = get_gift_mail(sender_name=gift_sender_name,
                              receiver_name=gift_reciver_name,
                              admin_email=admin_email)

    mail_mesg.attach(MIMEText(mail_plaintext, "plain"))
    mail_mesg.attach(MIMEText(mail_html, "html"))

    with smtplib.SMTP_SSL(_email_server,
                          port=465,
                          context=_email_context) as server:
        server.login(_internal_email, _email_auth_paswd)
        server.sendmail(_internal_email,
                        gift_sender_email,
                        mail_mesg.as_string())

