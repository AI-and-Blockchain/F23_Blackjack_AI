from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import regex as re

app = FastAPI()

user_bets = dict()

class FormItem(BaseModel):
    name: str
    # bet: str
    address: str

class betItem(BaseModel):
    address: str
    bet: int
    message: str

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
        item.name = "valid"
    # if bet.isdigit():
    #     item.bet = "valid"
    # else:
    #     item.bet = "invalid"
    if re.match(".*(0x[a-f,A-F,0-9]{40}).*", address):
        item.address = "valid"
    else:
        item.address = "invalid"
    # if item.bet == item.address == "valid":
    #     user_bets[address] = bet
    return item

# this is totally not a real thing anymore, but we will need some sort of getBet
# request to validate eventually 
@app.post("/getBet", response_model=betItem)
def get_bet(item: betItem):
    print(item)
    address = item.address
    bet = item.bet
    if address in user_bets:
        item.bet = int(user_bets[address])
        item.message = "valid"
    else:
        item.bet = 0
        item.message = "invalid"
    return item