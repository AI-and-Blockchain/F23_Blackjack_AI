from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import regex as re

app = FastAPI()

class FormItem(BaseModel):
    name: str
    bet: int
    address: str

@app.post("/F23_Blackjack_AI/frontend", response_model=dict)
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
        response_data = {
            "name": name,
            "bet": bet,
            "address": re.search(".*(0x[a-f,A-F,0-9]{40}).*", address).group(1),
        }
    else:
        response_data = {
            "name": name,
            "bet": "INVALID",
            "address": "INVALID"
        }
    print(response_data)
    return response_data
