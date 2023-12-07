from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import smtplib


def send_email(context: dict,
               sender_email: str,
               gift_sender: str,
               gift_receiver: str) -> None:
    mesg = MIMEMultipart("alternative")
    mesg["Subject"] = "Secret Santa"
    mesg["From"] = context.get("email")
    mesg["To"] = sender_email
    text = f"""
           Questa email è stata mandata automaticamente.
           {gift_sender}, dovrai fare il tuo regalo a {gift_receiver}
           """

    text_part = MIMEText(text, "plain")
    html_part = MIMEText(format_html_email(gift_sender, gift_receiver), "html")
    mesg.attach(text_part)
    mesg.attach(html_part)

    with smtplib.SMTP_SSL(context.get("server"), 465, context=context.get("context")) as server:
        server.login(context.get("email"), context.get("password"))
        server.sendmail(context.get("email"),
                        sender_email,
                        mesg.as_string())


def format_html_email(sender: str,
                      receiver: str) -> str:
    return f"""
        <html>
            <head>
                {css}
            </head>
            <body>
                <h1>Secret Santa</h1>
                <main>
                    {svg}
                    <p>{sender}, dovrai fare il tuo regalo a {receiver}.</p>
                </main>
                <footer>
                    <p>Questa email è stata inviata automaticamente.</p>
                    <a href="https://github.com/c4lopsitta/secretsanta">Visualizza codice sorgente dello script</a>
                </footer>
            </body>
        </html>
        """


css = """
<style>
* { margin: 0; padding: 0; }
body { display: flex; flex-flow: column; min-height: 100vh; }
main { margin: 0 2rem; width: calc(100vw - 4rem); display: grid; grid-template-columns: 1fr; grid-template-rows: 6fr 1fr; justify-content: center; align-items: center; }
main > * { display: flex; flex-flow: column; align-items: center; justify-content: center; }
svg { width: calc(100vw - 4rem) !important; height: 8rem !important; }
h1 { width: calc(100vw - 4rem); height: 4rem; background-color: #109020; color: #fafafa; margin: 2rem; display: flex; align-items: center; justify-content: center; }
footer { position: absolute; bottom: 0; margin: 2rem; height: 6rem; width: calc(100vw - 4rem); background-color: #dadadb; display: flex; flex-flow: column; align-items: center; justify-content: center; }
</style>
"""  # NOQA: E501

svg = """
<svg xmlns="http://www.w5.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#000000"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M4 17h16v2H4zm13-6.17L15.38 12 13 8.76 12 7.4l-1 1.36L8.62 12 7 10.83 9.08 8H4v6h16V8h-5.08z" opacity=".3"/><path d="M20 6h-2.18c.11-.31.18-.65.18-1 0-1.66-1.34-3-3-3-1.05 0-1.96.54-2.5 1.35l-.5.67-.5-.68C10.96 2.54 10.05 2 9 2 7.34 2 6 3.34 6 5c0 .35.07.69.18 1H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zm-5-2c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zM9 4c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm11 15H4v-2h16v2zm0-5H4V8h5.08L7 10.83 8.62 12 11 8.76l1-1.36 1 1.36L15.38 12 17 10.83 14.92 8H20v6z"/></svg>
"""  # NOQA: E501
