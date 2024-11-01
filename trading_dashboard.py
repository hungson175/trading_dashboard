from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import Optional
from app.models.futures import FuturesAccountResponse, FuturesOrdersResponse
from app.services.binance import BinanceService

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/get_my_name")
async def get_my_name():
    return {"name": "SonPH"}

@app.get("/get_futures_account", response_model=FuturesAccountResponse)
async def get_futures_account(
    x_api_key: str = Header(..., description="Binance API Key"),
    x_api_secret: str = Header(..., description="Binance API Secret")
):
    """
    Get Binance futures account information using API credentials.
    """
    try:
        return BinanceService.get_futures_account(x_api_key, x_api_secret)
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
        BinanceService.change_position_mode(x_api_key, x_api_secret, mode)
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
        return BinanceService.get_position_mode(x_api_key, x_api_secret)
    except Exception as e:
        return {"error": str(e)}

@app.get("/futures_get_all_orders", response_model=FuturesOrdersResponse)
async def futures_get_all_orders(
    x_api_key: str = Header(..., description="Binance API Key"),
    x_api_secret: str = Header(..., description="Binance API Secret"),
    symbol: Optional[str] = None,
    days: Optional[int] = 89
):
    """
    Get all futures orders for a given period.
    
    Parameters:
    - **x_api_key**: Your Binance API key (required)
    - **x_api_secret**: Your Binance API secret (required)
    - **symbol**: Trading pair symbol (e.g., 'BTCUSDT'). If not provided, returns orders for all symbols
    - **days**: Number of days to look back (default: 90, max: 90)
    
    Returns:
    - **total_orders**: Total number of orders in the response
    - **period**: Description of the time period
    - **orders**: List of orders with detailed information including:
        - orderId: Unique order identifier
        - symbol: Trading pair
        - status: Order status (e.g., 'FILLED')
        - price: Order price
        - avgPrice: Average fill price
        - origQty: Original quantity
        - executedQty: Executed quantity
        - realizedPnl: Realized profit/loss
        - commission: Trading fee
        - and more order details
    """
    try:
        result = BinanceService.get_all_orders(x_api_key, x_api_secret, symbol, days)
        print(f"API Response: {result}")  # Add logging to debug
        return result
    except Exception as e:
        print(f"Error in futures_get_all_orders: {str(e)}")  # Add error logging
        return {"error": str(e), "detail": "Internal server error occurred"}


