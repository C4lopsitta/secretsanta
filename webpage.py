from typing import Annotated

from fastapi import FastAPI, Form
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import santastores
from santastores import writer_queue

app = FastAPI()
app.mount("/templates", StaticFiles(directory="templates"), name="templates")
templates = Jinja2Templates(directory="templates")


@app.get('/')
def join_store(request: Request,
               name: str = "",
               email_address: str = "",
               store_id: str = None):
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
            "email_address": email_address
        }
    )

@app.post("/")
def store_data(request: Request,
               name: Annotated[str, Form()],
               email_address: Annotated[str, Form()],
               store_id: Annotated[str, Form()]):


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
                  store_id: str | None = None,):
    pass



