from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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
    response_data = {
        "name": name,
        "bet": bet,
        "address": address,
    }
    print(response_data)
    return response_data
