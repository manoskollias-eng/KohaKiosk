from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.sip2_client import DemoSIP2Client

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title="KohaKiosk")

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "ui")),
    name="static"
)

templates = Jinja2Templates(
    directory=str(BASE_DIR / "ui")
)

client = DemoSIP2Client()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.get("/checkout", response_class=HTMLResponse)
async def checkout_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="checkout.html",
        context={}
    )


@app.post("/checkout", response_class=HTMLResponse)
async def checkout_action(
    request: Request,
    patron_barcode: str = Form(...),
    item_barcode: str = Form(...)
):

    result = client.checkout(
        patron_barcode,
        item_barcode
    )

    return templates.TemplateResponse(
        request=request,
        name="checkout.html",
        context={
            "result": result
        }
    )


@app.get("/checkin", response_class=HTMLResponse)
async def checkin_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="checkin.html",
        context={}
    )


@app.post("/checkin", response_class=HTMLResponse)
async def checkin_action(
    request: Request,
    item_barcode: str = Form(...)
):

    result = client.checkin(item_barcode)

    return templates.TemplateResponse(
        request=request,
        name="checkin.html",
        context={
            "result": result
        }
    )


@app.get("/health")
async def health():

    return {
        "status": "ok",
        "application": "KohaKiosk",
        "version": "0.1"
    }