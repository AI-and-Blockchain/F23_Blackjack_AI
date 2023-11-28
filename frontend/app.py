from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import regex as re

from model.game import BlackjackGame
from model.player import WebUser, QAgent
from blockchain.blockchain import BlockchainInterface

app = FastAPI()

class FormItem(BaseModel):
    name: str
    address: str
    smartness: int

class betItem(BaseModel):
    address: str
    bet: int
    message: str

class playerInfo(BaseModel):
    username: str
    address: str
    bet: int
    aiName: str

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

class userBalance(BaseModel):
    address: str
    balance: int

class addressItem(BaseModel):
    address: str

class byteCode(BaseModel):
    func: str

class smartnessStorage(BaseModel):
    smartness: float


user = playerInfo(username='', address='', bet=0, aiName="")
game = BlackjackGame()
smartness = smartnessStorage(smartness=0.0)
with open("blockchain/address.txt") as f:
    contract = BlockchainInterface(f.read().strip())

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
    smartness.smartness = item.smartness / 100
    user.aiName = "Godlike AI" if item.smartness == 100 else "Super Smart AI" if item.smartness > 70 else "Pretty Good AI" if item.smartness > 40 else "Beginner AI" if item.smartness > 10 else "Fresh Off the Compiler AI"

    if name == '':
        item.name = "invalid"
    else:
        user.username = item.name
        item.name = "valid"

    if item.name == "valid":
        user.address = item.address
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
    game.add_players([WebUser(user.username, user.bet, user.address), QAgent(name=user.aiName, smartness=smartness.smartness, trainable=False)])
    return user

@app.post("/results", response_model=resultsItem)
def results():
    return resultsItem(data = game.results())

@app.post("/getBalance", response_model=userBalance)
def getBalance(item: userBalance):
    item.balance = contract.getBalance(item.address)
    return item

@app.post("/trackTransaction", response_model=addressItem)
async def getBalance(item: addressItem):
    await contract.watchForTransaction(item.address)
    return item

@app.post("/contractAddress", response_model=addressItem)
async def getAddress():
    return addressItem(address=contract.address)

@app.post("/owner", response_model=addressItem)
async def getOwner():
    with open("blockchain/owner.txt", 'r') as f:
        return addressItem(address=f.read().strip())

@app.post("/byteCode", response_model=byteCode)
async def convert(item: byteCode):
    return byteCode(func=contract.getByteCode(item.func))

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("frontend/static/assets/favicon.ico")