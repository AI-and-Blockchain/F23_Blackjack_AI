from fastapi import FastAPI
from fastapi.responses import RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sys


from model.game import BlackjackGame
from model.player import WebUser, QAgent, LocalPlayer
from blockchain.blockchain import BlockchainInterface

# if there is no custom agent file to import yet, make a 50/50 agent and import it
try:
    import model.CustomAgent
except:
    with open("model/CustomAgentExample.py", 'r') as f:
        with open("model/CustomAgent.py", 'w') as f2:
            f2.write(f.read())
    import model.CustomAgent

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
    players: int
    aiName: str
    secondAiName: str

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

class fileContents(BaseModel):
    file: str

class playerCount(BaseModel):
    players: int

# ensures that the agent will not fail on normal gameplay calls
# is always called in a try-except to ensure that it will not break the backend
def testAgent():
    del sys.modules["model.CustomAgent"]
    import model.CustomAgent
    agent = model.CustomAgent.CustomAgent("test")
    if not (agent.id == str(agent) == repr(agent) == "test"):
        raise Exception
    agent.add_card(1, 11)
    agent.add_card(2, 13)
    agent.add_dealer_card(1)
    if agent.decision() == None:
        raise Exception
    localPlayer = LocalPlayer(model.CustomAgent.CustomAgent("test"))
    localPlayer.deal(1)
    localPlayer.deal(2)
    localPlayer.add_dealer_card(1)
    localPlayer.hit(1)
    localPlayer.decision()
    localPlayer.start_new()

# define some json models to be used later, as well as the game and blockchain items
user = playerInfo(username='', address='', bet=0, players=2, aiName="", secondAiName="")
game = BlackjackGame()
smartness = smartnessStorage(smartness=0.0)
with open("blockchain/address.txt") as f:
    contract = BlockchainInterface(f.read().strip())

app.mount('/frontend/static', StaticFiles(directory='frontend/static', html=True), name='static')

# set a redirect from any extraneous urls to the login screen
@app.get("/")
@app.get("/frontend")
@app.get("/frontend/static")
async def redirect():
    return RedirectResponse("http://127.0.0.1:8000/frontend/static/Login.html")

# save the player and AIs' information
@app.post("/login", response_model=FormItem)
def submit_form(item: FormItem):
    game.revert()
    name = item.name
    smartness.smartness = item.smartness / 100
    user.aiName = "Lord Blackjack" if item.smartness == 100 else "Master Mind AI" if item.smartness > 70 else "JokerPoker AI" if item.smartness == 69 else "Ninja AI" if item.smartness > 40 else "NPC AI" if item.smartness > 10 else "Fresh Off the Compiler AI"

    if name == '':
        item.name = "invalid"
    else:
        user.username = item.name
        item.name = "valid"

    if item.name == "valid":
        user.address = item.address
        user.bet = 0
    return item

# ngl this isn't even needed anymore but i cant be bothered to refactor to dodge it
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

# send the information of the deal to the frontend
@app.post("/deal", response_model=dealInfo)
def deal():
    info = dealInfo(dealer = [], players = [])
    info.dealer, info.players = game.deal()
    return info

# send the player's card and status to the frontend
@app.post("/hit", response_model=playInfo)
def hit():
    info = playInfo(card = 0, status = True)
    info.card, info.status = game.play_user("H")
    return info

# send that the player is done to the frontend
@app.post("/stand", response_model=playInfo)
def stand():
    info = playInfo(card = 0, status = True)
    info.card, info.status = game.play_user("S")
    return info

# send the Ai's moves to the frontend
@app.post("/AI", response_model=cardInfo)
def AI():
    info = cardInfo(cards = [])
    info.cards = game.play_AI()
    return info

# send the dealer's moves to the frontend
@app.post("/dealer", response_model=cardInfo)
def AI():
    info = cardInfo(cards = [])
    info.cards = game.play_dealer()
    return info

# sends all information obtained from the login page to the blackjack page
@app.post("/playerData", response_model=playerInfo)
def playerData():
    playersToAdd = [WebUser(user.username, user.bet, user.address), QAgent(name=user.aiName, smartness=smartness.smartness, trainable=False)]
    if user.players == 3:
        playersToAdd.append(model.CustomAgent.CustomAgent(user.secondAiName))
    game.add_players(playersToAdd)
    return user

# sends the results (wins and losses) to the frontend
@app.post("/results", response_model=resultsItem)
def results():
    return resultsItem(data = game.results())

# sends the user's balance to the frontend
@app.post("/getBalance", response_model=userBalance)
def getBalance(item: userBalance):
    item.balance = contract.getBalance(item.address)
    return item

# watches a blockchain transaction until it is finished, then returns
@app.post("/trackTransaction", response_model=addressItem)
async def getBalance(item: addressItem):
    await contract.watchForTransaction(item.address)
    return item

# returns the address of the smart contract
@app.post("/contractAddress", response_model=addressItem)
async def getAddress():
    return addressItem(address=contract.address)

# returns the wallet address of the owner
@app.post("/owner", response_model=addressItem)
async def getOwner():
    with open("blockchain/owner.txt", 'r') as f:
        return addressItem(address=f.read().strip())

# converts a given string to bytecode (to determine function selectors)
@app.post("/byteCode", response_model=byteCode)
async def convert(item: byteCode):
    return byteCode(func=contract.getByteCode(item.func))

# tests the uploaded agent and ensures that it meets standards
@app.post('/upload', response_model=playerCount)
async def fileInput(item: fileContents):
    with open("model/CustomAgent.py", 'w') as f:
        f.write(item.file.replace("\r", ''))
    try:
        testAgent()
    except:
        return playerCount(players=user.players)
    user.players = 3
    user.secondAiName = user.username + "'s" + " Agent"
    return playerCount(players=user.players)

# resets the game to have two players
@app.post("/resetUpload")
async def resetUpload():
    user.players = 2
    user.secondAiName = ''
    del sys.modules["model.CustomAgent"]
    with open("model/CustomAgentExample.py", 'r') as f:
        with open("model/CustomAgent.py", 'w') as f2:
            f2.write(f.read())
    import model.CustomAgent

# returns the favicon to use as the tab icon
@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse("frontend/static/assets/favicon.ico")
