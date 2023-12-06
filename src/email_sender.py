from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import smtplib
import ssl


def send_email(context: ssl.SSLContext,
               smtp_url: str,
               login_email: str,
               login_password: str,
               sender_email: str,
               gift_sender: str,
               gift_receiver: str) -> None:
    mesg = MIMEMultipart("alternative")
    mesg["Subject"] = "Secret Santa"
    mesg["From"] = login_email
    mesg["To"] = sender_email
    text = f"""
           Questa email è stata mandata automaticamente.
           {gift_sender}, dovrai fare il tuo regalo a {gift_receiver}
           """

    text_part = MIMEText(text, "plain")
    html_part = MIMEText(format_html_email(gift_sender, gift_receiver), "html")
    mesg.attach(text_part)
    mesg.attach(html_part)

    with smtplib.SMTP_SSL(smtp_url, 465, context=context) as server:
        server.login(login_email, login_password)
        server.sendmail(login_email,
                        sender_email,
                        mesg.as_string())


def format_html_email(sender: str,
                      receiver: str) -> str:
    return f"""
        <html>
            <head>

            </head>
            <body>
                <h1>Secret Santa</h1>
                <p>{sender}, dovrai fare il tuo regalo a {receiver}.</p>
                <footer>
                    <p>Questa email è stata inviata automaticamente.</p>
                    <a href="https://github.com/c4lopsitta/secretsanta">Visualizza codice sorgente dello script</a>
                </footer>
            </body>
        </html>
        """
