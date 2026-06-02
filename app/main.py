from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
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

templates = Jinja2Templates(directory=str(BASE_DIR / "ui"))

client = DemoSIP2Client()

checkout_session = {
    "patron_barcode": "",
    "items": []
}


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
        context={
            "session": checkout_session,
            "result": None
        }
    )


@app.post("/checkout/set-patron")
async def set_patron(patron_barcode: str = Form(...)):
    checkout_session["patron_barcode"] = patron_barcode.strip()
    checkout_session["items"] = []
    return RedirectResponse("/checkout", status_code=303)


@app.post("/checkout/add-item")
async def add_item(item_barcode: str = Form(...)):

    item_barcode = item_barcode.strip()

    info = client.item_info(item_barcode)

    if info["success"]:

        exists = False

        for item in checkout_session["items"]:
            if item["barcode"] == item_barcode:
                exists = True
                break

        if not exists:
            checkout_session["items"].append({
                "barcode": item_barcode,
                "title": info["title"]
            })

    return RedirectResponse("/checkout", status_code=303)


@app.post("/checkout/complete", response_class=HTMLResponse)
async def complete_checkout(request: Request):

    patron_barcode = checkout_session["patron_barcode"]
    items = checkout_session["items"]

    results = []

    for item in items:

        result = client.checkout(
            patron_barcode,
            item["barcode"]
        )

        result["barcode"] = item["barcode"]

        results.append(result)

    checkout_session["items"] = []

    return templates.TemplateResponse(
        request=request,
        name="checkout.html",
        context={
            "session": checkout_session,
            "results": results
        }
    )


@app.post("/checkout/clear")
async def clear_checkout():

    checkout_session["patron_barcode"] = ""
    checkout_session["items"] = []

    return RedirectResponse("/checkout", status_code=303)


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

@app.get("/account", response_class=HTMLResponse)
async def account_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="account.html",
        context={
            "patron": None
        }
    )


@app.post("/account", response_class=HTMLResponse)
async def account_lookup(
    request: Request,
    patron_barcode: str = Form(...)
):

    result = client.patron_info(patron_barcode)

    if not result["success"]:

        return templates.TemplateResponse(
            request=request,
            name="account.html",
            context={
                "patron": None
            }
        )

    patron = result["patron"]

    loan_titles = []

    for barcode in patron["loans"]:

        info = client.item_info(barcode)

        if info["success"]:
            loan_titles.append(info["title"])

    return templates.TemplateResponse(
        request=request,
        name="account.html",
        context={
            "patron": patron,
            "loans": loan_titles
        }
    ) 
@app.get("/health")
async def health():

    return {
        "status": "ok",
        "application": "KohaKiosk",
        "version": "0.3"
    }