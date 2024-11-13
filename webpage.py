from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import santastores

app = FastAPI()
app.mount("/templates", StaticFiles(directory="templates"), name="templates")
templates = Jinja2Templates(directory="templates")


@app.get('/')
def join_store(request: Request,
               name: str = "",
               email_address: str = "",
               store_id: str = None):
    if store_id is None:
        return HTMLResponse(content=templates.TemplateResponse(
            request=request,
            name="no_store_id.html"
        ))

    # there's a store, load it
    santastore = santastores.load_store(store_id)

    return HTMLResponse(content=templates.TemplateResponse(
        request=request,
        name="join_store.html",
        context={
            "store_id": store_id,
            "name": name,
            "email_address": email_address
        }
    ))



