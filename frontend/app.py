from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import regex as re

app = FastAPI()


class FormItem(BaseModel):
    name: str
    # bet: str
    address: str

class betItem(BaseModel):
    address: str
    bet: int
    message: str

class playerInfo(BaseModel):
    username: str
    address: str
    bet: int

user = playerInfo(username='', address='', bet=0)

app.mount('/frontend/static', StaticFiles(directory='frontend/static', html=True), name='static')

@app.get("/")
@app.get("/frontend")
@app.get("/frontend/static")
async def redirect():
    return RedirectResponse("http://127.0.0.1:8000/frontend/static/Login.html")

@app.post("/login", response_model=FormItem)
def submit_form(item: FormItem):
    # Access the submitted form data as an object
    name = item.name
    # bet = item.bet
    address = item.address
    #name
    #bet
    #metamask wallet id
    
    # You can process and use the form data as needed
    # In this example, just returning it as a response
    # result = responseItem()
    if name == '':
        item.name = "invalid"
    else:
        user.username = item.name
        item.name = "valid"
    # if bet.isdigit():
    #     item.bet = "valid"
    # else:
    #     item.bet = "invalid"
    if re.match(".*(0x[a-f,A-F,0-9]{40}).*", address):
        user.address = item.address
        item.address = "valid"
    else:
        item.address = "invalid"
    if item.name == item.address == "valid":
        user.bet = 0
    return item

@app.post("/setBet", response_model=betItem)
def set_bet(item: betItem):
    print(item)
    address = item.address
    if user.address == address:
        user.bet = int(item.bet)
        item.message = "valid"
    else:
        item.message = "invalid"
    return item


@app.post("/playerData", response_model=playerInfo)
def playerData():
    return user
    