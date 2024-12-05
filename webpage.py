import os
import re
import uuid
from datetime import datetime
from os import getenv
from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import JSONResponse

import email_sender
import santastores
from SantaEntry import SantaEntry
from santastores import writer_queue, add_santa_entry

base_url = getenv("BASE_URL")
admin_email = getenv("ADMIN_EMAIL")

app = FastAPI()
app.mount("/templates", StaticFiles(directory="templates"), name="templates")
templates = Jinja2Templates(directory="templates")


@app.get('/')
def join_store(request: Request,
               name: str = "",
               email_address: str = "",
               store_id: str = None,
               name_error: str = "",
               email_error: str = ""):
    if store_id is None:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            status_code=404,
            context={
                "id": None,
                "error_text": "A santa store id is required. Ask the organiser for the correct link.",
                "error_title": "No Store Id",
                "error_code": "NO_STORE_ID"
            }
        )

    if os.getenv("debug") != "true" and store_id == "test":
        return JSONResponse(
            status_code=400,
            content={
                "error": "Debugging mode is disabled. Testing unavailable"
            }
        )

    # there's a store, load it
    try:
        santastore = santastores.load_store(store_id)
    except Exception as e:
        print(e.__str__())
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            status_code=404,
            context={
                "id": store_id,
                "error_title": "Invalid store id",
                "error_code": "INVALID_STORE_ID",
                "error_text": f"The given id {store_id} was not found."
            }
        )

    return templates.TemplateResponse(
        request=request,
        name="join_store.html",
        context={
            "id": store_id,
            "store_name": santastore["name"],
            "store_id": store_id,
            "name": name,
            "email_address": email_address,
            "name_error": name_error,
            "email_error": email_error
        }
    )


@app.post("/")
def accept_registration(request: Request,
                        name: Annotated[str, Form()],
                        email_address: Annotated[str, Form()],
                        store_id: Annotated[str, Form()]):
    if os.getenv("debug") != "true" and store_id == "test":
        return JSONResponse(
            status_code=400,
            content={
                "error": "Debugging mode is disabled. Testing unavailable"
            }
        )

    name_error, email_error = None, None

    if re.fullmatch(r"^[a-zA-Zà-žÀ-Ž\s]+$", name) is None or len(name) > 30:
        name_error = "Il nome può solamente contenere caratteri dell'alfabeto con spazi ed un massimo di 30 caratteri."

    if re.fullmatch(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email_address) is None:
        email_error = "L'email non è valida"

    if name_error or email_error:
        return RedirectResponse(
            status_code=303,
            url=f"/?store_id={store_id}&email_error={email_error if email_error else ''}&name_error={name_error if name_error else ''}"
        )

    try:
        santastore = santastores.load_store(store_id)

        for user in santastore["people"]:
            if user["name"] == name and user["email_address"] == email_address or user["email_address"] == email_address:
                return templates.TemplateResponse(
                    request=request,
                    name="error.html",
                    context={
                        "id": store_id,
                        "error_title": "Iscrizione già effettuata",
                        "error_text": f"L'iscrizione per l'email <p class=\"text-monospace\">{email_address}</p> è già stata effettuata. Se ci sono problemi, contatta l'amministratore",
                        "error_code": "REGISTRATION_ALREADY_COMPLETED"
                    }
                )
    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            status_code=404,
            context={
                "id": store_id,
                "error_text": f"Il gruppo con ID {store_id} non è stato trovato.",
                "error_title": "Gruppo non trovato",
                "error_code": "INVALID_STORE_ID"
            }
        )

    try:
        email_sender.send_confirmation_email(sender_name=name,
                                             sender_email=email_address,
                                             url=f"{base_url}/confirm_email?store_id={store_id}&email_address={email_address}&name={name}",
                                             retry_url=f"{base_url}/?store_id={store_id}&email_address={email_address}&name={name}",
                                             admin_email=admin_email,
                                             store_name=santastore["name"])

    except Exception as e:
        trace_id = uuid.uuid4()
        print(f"""
[ERROR] Could not send confirmation email to {email_address}.
[INFO] Trace id: {trace_id}
[INFO] Error:
{e.__str__()}
""")
        return templates.TemplateResponse(
            request=request,
            status_code=500,
            name="error.html",
            context={
                "id": None,
                "error_text": "Invio email",
                "error_title": f"Errore durante l'invio della mail di conferma. Contatta l'amministratore e fornisci il seguente codice<br><p class=\"text-monospace\">{trace_id}</p>",
                "error_code": "CONFIRM_EMAIL_SEND_ERROR"
            }
        )

    return templates.TemplateResponse(
        request=request,
        status_code=202,
        name="register.html",
        context={
            "id": store_id,
            "name": name,
            "email_address": email_address
        }
    )


@app.get("/confirm_email")
def confirm_email(request: Request,
                  name: str,
                  email_address: str,
                  store_id: str | None = None):
    store = santastores.load_store(store_id)
    print(f"[INFO] Recieved registration by user {email_address}, name is {name}")

    if os.getenv("debug") != "true" and store_id == "test":
        return templates.TemplateResponse(
            request=request,
            status_code=400,
            name="error.html",
            context={
                "id": None,
                "error_text": "Modalità di debug disabilitata",
                "error_title": f"La modalità di debug è disabilitata. Non è possibile utilizzare la store test",
                "error_code": "DEBUG_MODE_OFF"
            }
        )

    for user in store["people"]:
        if user["name"] == name and user["email_address"] == email_address:
            return templates.TemplateResponse(
                request=request,
                name="confirmed.html",
                context={
                    "id": store_id,
                    "name": name,
                    "store_name": store["name"],
                    "date": datetime.fromisoformat(store.get("end_date")).strftime("%d di Dicembre"),
                }
            )

    entry = SantaEntry(name=name,
                       email_address=email_address,
                       store_id=store_id)

    add_santa_entry(entry)

    return templates.TemplateResponse(
        request=request,
        name="confirmed.html",
        context={
            "id": store_id,
            "name": name,
            "store_name": store["name"],
            "date": datetime.fromisoformat(store.get("end_date")).strftime("%d di Dicembre"),
        }
    )
