import ssl
from os import getenv

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import smtplib


_internal_email = getenv("EMAIL")
_email_auth_paswd = getenv("EMAIL_PASSWORD")
_email_server = getenv("EMAIL_SERVER")
_email_context = ssl.create_default_context()


def get_gift_mail(sender_name: str,
                  receiver_name: str,
                  admin_email: str) -> str:
    with open("templates/emails/gift.html", "r") as f:
        html = f.read()
    return (html.replace("{{ sender_name }}", sender_name)
            .replace("{{ receiver_name }}", receiver_name)
            .replace("{{ admin_email }}", admin_email))


def get_confirmation_mail(sender_name: str,
                          sender_email: str,
                          url: str,
                          retry_url,
                          store_name: str,
                          admin_email: str) -> str:
    with open("templates/emails/confirm.html", "r") as f:
        html = f.read()
    return (html.replace("{{ sender_name }}", sender_name)
            .replace("{{ sender_email }}", sender_email)
            .replace("{{ store_name }}", store_name)
            .replace("{{ url }}", url)
            .replace("{{ retry_url }}", retry_url)
            .replace("{{ admin_email }}", admin_email))


def send_confirmation_email(sender_name: str,
                            sender_email: str,
                            url: str,
                            retry_url: str,
                            store_name: str,
                            admin_email: str):
    _construct_and_send_mail(
        html=get_confirmation_mail(sender_name, sender_email, url, retry_url, store_name, admin_email),
        plain=url,
        subject="Secret Santa - Conferma la tua iscrizione",
        to=sender_email)


def send_gift_mail(gift_sender_name: str,
                   gift_sender_email: str,
                   gift_reciver_name: str,
                   admin_email: str):
    _construct_and_send_mail(html=get_gift_mail(gift_sender_name, gift_reciver_name, admin_email),
                             plain=f"{gift_sender_name}, dovrai fare il tuo regalo a {gift_reciver_name}!",
                             subject="Secret Santa",
                             to=gift_sender_email)


def _construct_and_send_mail(html,
                             plain,
                             subject: str,
                             to: str):
    mesg = MIMEMultipart("alternative")
    mesg["Subject"] = subject
    mesg["From"] = _internal_email
    mesg["To"] = to
    mesg.attach(MIMEText(plain, "plain"))
    mesg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL(_email_server,
                          port=465,
                          context=_email_context) as server:
        server.login(_internal_email, _email_auth_paswd)
        server.sendmail(_internal_email,
                        to,
                        mesg.as_string())
