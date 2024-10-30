from fastapi import FastAPI, Request, Header
from binance import Client
from dotenv import load_dotenv
import os
import uvicorn

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

@app.get("/get_my_name")
async def get_my_name():
    return {"name": "SonPH"}

@app.get("/get_futures_account")
async def get_futures_account(
    x_api_key: str = Header(..., description="Binance API Key"),
    x_api_secret: str = Header(..., description="Binance API Secret")
):
    """Get Binance futures account information using API credentials"""
    try:
        # Initialize Binance client
        client = Client(x_api_key, x_api_secret)
        
        # Get futures account information
        account_info = client.futures_account()
        # Filter assets and positions
        account_info["assets"] = [asset for asset in account_info["assets"] if asset["updateTime"] > 0]
        account_info["positions"] = [position for position in account_info["positions"] if float(position["initialMargin"]) > 0]
        return account_info
    except Exception as e:
        return {"error": str(e)}

@app.post("/futures_change_position_mode")
async def futures_change_position_mode(
    mode: bool,
    x_api_key: str = Header(..., description="Binance API Key"), 
    x_api_secret: str = Header(..., description="Binance API Secret")
):
    """Change position mode between Hedge Mode (true) and One-way Mode (false)"""
    try:
        client = Client(x_api_key, x_api_secret)
        client.futures_change_position_mode(dualSidePosition=mode)
        return {"message": f"Hedge mode changed to {mode}"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/futures_get_position_mode")
async def futures_get_position_mode(
    x_api_key: str = Header(..., description="Binance API Key"),
    x_api_secret: str = Header(..., description="Binance API Secret")
):
    """Get current position mode"""
    try:
        client = Client(x_api_key, x_api_secret)
        mode = client.futures_get_position_mode()
        return mode
    except Exception as e:
        return {"error": str(e)}

# ... rest of your endpoints following the same pattern
