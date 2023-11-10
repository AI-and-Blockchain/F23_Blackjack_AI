from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel
import regex as re

app = FastAPI()


class FormItem(BaseModel):
    name: str
    bet: int
    address: str

app.mount('/static', StaticFiles(directory='static', html=True), name='static')

# from starlette.responses import FileResponse 

# @app.get("/")
# async def read_index():
#     return FileResponse('Blackjack.html')

@app.post("/F23_Blackjack_AI/frontend", response_model=str)
def submit_form(item: FormItem):
    # Access the submitted form data as an object
    name = item.name
    bet = item.bet
    address = item.address
    #name
    #bet
    #metamask wallet id
    
    # You can process and use the form data as needed
    # In this example, just returning it as a response
    if re.match(".*(0x[a-f,A-F,0-9]{40}).*", address):
        return "valid"
    else:
        return "invalid"
    # print(response_data)
    # return response_data
