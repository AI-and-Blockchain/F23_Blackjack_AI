from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import regex as re

from model.game import BlackjackGame
from model.player import WebUser, QAgent

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

class dealInfo(BaseModel):
    dealer: list
    players: list

class cardInfo(BaseModel):
    cards: list

class playInfo(BaseModel):
    card: int
    status: bool

class resultsItem(BaseModel):
    data: list


user = playerInfo(username='', address='', bet=0)
game = BlackjackGame()

app.mount('/frontend/static', StaticFiles(directory='frontend/static', html=True), name='static')

@app.get("/")
@app.get("/frontend")
@app.get("/frontend/static")
async def redirect():
    return RedirectResponse("http://127.0.0.1:8000/frontend/static/Login.html")

@app.post("/login", response_model=FormItem)
def submit_form(item: FormItem):
    game.revert()
    name = item.name
    address = item.address

    if name == '':
        item.name = "invalid"
    else:
        user.username = item.name
        item.name = "valid"
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
    address = item.address
    if user.address == address:
        user.bet = int(item.bet)
        item.message = "valid"
        game.bet()
        game.start()
    else:
        item.message = "invalid"
    return item

@app.post("/deal", response_model=dealInfo)
def deal():
    info = dealInfo(dealer = [], players = [])
    info.dealer, info.players = game.deal()
    return info


@app.post("/hit", response_model=playInfo)
def hit():
    info = playInfo(card = 0, status = True)
    info.card, info.status = game.play_user("H")
    return info


@app.post("/stand", response_model=playInfo)
def stand():
    info = playInfo(card = 0, status = True)
    info.card, info.status = game.play_user("S")
    return info

@app.post("/AI", response_model=cardInfo)
def AI():
    info = cardInfo(cards = [])
    info.cards = game.play_AI()
    return info

@app.post("/dealer", response_model=cardInfo)
def AI():
    info = cardInfo(cards = [])
    info.cards = game.play_dealer()
    return info


@app.post("/playerData", response_model=playerInfo)
def playerData():
    game.add_players([WebUser(user.username, user.bet, user.address), QAgent()])
    return user

@app.post("/results", response_model=playerInfo)
def results():
    return resultsItem(data = game.results())


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("frontend/static/assets/favicon.ico")