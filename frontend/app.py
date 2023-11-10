from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import regex as re

app = FastAPI()


class FormItem(BaseModel):
    name: str
    bet: int
    address: str

app.mount('/frontend/static', StaticFiles(directory='frontend/static', html=True), name='static')

@app.get("/")
@app.get("/frontend")
@app.get("/frontend/static")
async def redirect():
    return RedirectResponse("http://127.0.0.1:8000/frontend/static/Login.html")

@app.post("/login", response_model=str)
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
