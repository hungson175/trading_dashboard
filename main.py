from fastapi import FastAPI, Request, Header
from binance import Client
from dotenv import load_dotenv
import os
import uvicorn
from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Pydantic models for response structure
class AssetInfo(BaseModel):
    asset: str
    walletBalance: str
    unrealizedProfit: str
    marginBalance: str
    maintMargin: str
    initialMargin: str
    positionInitialMargin: str
    openOrderInitialMargin: str
    maxWithdrawAmount: str
    crossWalletBalance: str
    crossUnPnl: str
    availableBalance: str
    marginAvailable: bool
    updateTime: int

class PositionInfo(BaseModel):
    symbol: str
    initialMargin: str
    maintMargin: str
    unrealizedProfit: str
    positionInitialMargin: str
    openOrderInitialMargin: str
    leverage: str
    isolated: bool
    entryPrice: str
    breakEvenPrice: str
    maxNotional: str
    positionSide: str
    positionAmt: str
    notional: str
    isolatedWallet: str
    updateTime: int
    bidNotional: str
    askNotional: str

class FuturesAccountResponse(BaseModel):
    feeTier: int
    canTrade: bool
    canDeposit: bool
    canWithdraw: bool
    feeBurn: bool
    tradeGroupId: int
    updateTime: int
    multiAssetsMargin: bool
    totalInitialMargin: str
    totalMaintMargin: str
    totalWalletBalance: str
    totalUnrealizedProfit: str
    totalMarginBalance: str
    totalPositionInitialMargin: str
    totalOpenOrderInitialMargin: str
    totalCrossWalletBalance: str
    totalCrossUnPnl: str
    availableBalance: str
    maxWithdrawAmount: str
    assets: List[AssetInfo]
    positions: List[PositionInfo]

    class Config:
        json_schema_extra = {
            "example": {
                "feeTier": 0,
                "canTrade": True,
                "canDeposit": True,
                "canWithdraw": True,
                "feeBurn": True,
                "tradeGroupId": -1,
                "updateTime": 0,
                "multiAssetsMargin": False,
                "totalInitialMargin": "29.01981656",
                "totalMaintMargin": "0.58039633",
                "totalWalletBalance": "8459.32092583",
                "totalUnrealizedProfit": "0.81348284",
                "totalMarginBalance": "8460.13440867",
                "totalPositionInitialMargin": "29.01981656",
                "totalOpenOrderInitialMargin": "0.00000000",
                "totalCrossWalletBalance": "8459.32092583",
                "totalCrossUnPnl": "0.81348284",
                "availableBalance": "8431.11459211",
                "maxWithdrawAmount": "8431.11459211",
                "assets": [
                    {
                        "asset": "BNB",
                        "walletBalance": "0.01849866",
                        "unrealizedProfit": "0.00000000",
                        "marginBalance": "0.01849866",
                        "maintMargin": "0.00000000",
                        "initialMargin": "0.00000000",
                        "positionInitialMargin": "0.00000000",
                        "openOrderInitialMargin": "0.00000000",
                        "maxWithdrawAmount": "0.01849866",
                        "crossWalletBalance": "0.01849866",
                        "crossUnPnl": "0.00000000",
                        "availableBalance": "0.01849866",
                        "marginAvailable": True,
                        "updateTime": 1730318811018
                    },
                    {
                        "asset": "USDT",
                        "walletBalance": "8459.32092583",
                        "unrealizedProfit": "0.81348284",
                        "marginBalance": "8460.13440867",
                        "maintMargin": "0.58039633",
                        "initialMargin": "29.01981656",
                        "positionInitialMargin": "29.01981656",
                        "openOrderInitialMargin": "0.00000000",
                        "maxWithdrawAmount": "8431.11459211",
                        "crossWalletBalance": "8459.32092583",
                        "crossUnPnl": "0.81348284",
                        "availableBalance": "8431.11459211",
                        "marginAvailable": True,
                        "updateTime": 1729518843031
                    }
                ],
                "positions": [
                    {
                        "symbol": "BTCUSDT",
                        "initialMargin": "29.01981656",
                        "maintMargin": "0.58039633",
                        "unrealizedProfit": "0.81348284",
                        "positionInitialMargin": "29.01981656",
                        "openOrderInitialMargin": "0",
                        "leverage": "5",
                        "isolated": False,
                        "entryPrice": "72142.8",
                        "breakEvenPrice": "72175.26426",
                        "maxNotional": "480000000",
                        "positionSide": "LONG",
                        "positionAmt": "0.002",
                        "notional": "145.09908284",
                        "isolatedWallet": "0",
                        "updateTime": 1730318811018,
                        "bidNotional": "0",
                        "askNotional": "0"
                    }
                ]
            }
        }

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
    
    Returns detailed information about your futures account including:
    - Account details (fee tier, permissions, etc.)
    - Balance information
    - Active assets
    - Open positions
    """
    try:
        client = Client(x_api_key, x_api_secret)
        account_info = client.futures_account()
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

@app.get("/futures_get_all_orders")
async def futures_get_all_orders(
    x_api_key: str = Header(..., description="Binance API Key"),
    x_api_secret: str = Header(..., description="Binance API Secret"),
    symbol: str = None,
    days: Optional[int] = 90
):
    try:
        # Enforce 90-day limit
        if days > 90:
            return {
                "error": "Binance only allows fetching orders from the last 90 days",
                "requested_days": days,
                "maximum_days": 90
            }

        client = Client(x_api_key, x_api_secret)
        end_time = int(datetime.now().timestamp() * 1000)
        start_time = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
        
        all_orders = []
        all_trades = {}
        
        # Get all orders with 7-day chunks
        current_end_time = end_time
        while current_end_time > start_time:
            chunk_start_time = max(
                start_time,
                current_end_time - (7 * 24 * 60 * 60 * 1000)
            )
            
            # Get orders for current chunk
            params = {
                "symbol": "BTCUSDT" if not symbol else symbol,
                "startTime": chunk_start_time,
                "endTime": current_end_time,
                "limit": 1000
            }
            
            orders = client.futures_get_all_orders(**params)
            
            # Get corresponding trades for PnL data
            trades = client.futures_account_trades(**params)
            
            # Map trades by orderId for easy lookup
            for trade in trades:
                order_id = trade["orderId"]
                if order_id not in all_trades:
                    all_trades[order_id] = []
                all_trades[order_id].append(trade)
            
            all_orders.extend(orders)
            current_end_time = chunk_start_time - 1

        # Add PnL data to orders
        for order in all_orders:
            order["timeReadable"] = datetime.fromtimestamp(order["time"] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            if "updateTime" in order:
                order["updateTimeReadable"] = datetime.fromtimestamp(order["updateTime"] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            
            # Add PnL data if available
            order_trades = all_trades.get(order["orderId"], [])
            if order_trades:
                realized_pnl = sum(float(trade.get("realizedPnl", 0)) for trade in order_trades)
                order["realizedPnl"] = str(realized_pnl)
                
                # Add commission information
                commission = sum(float(trade.get("commission", 0)) for trade in order_trades)
                order["commission"] = str(commission)
                if order_trades[0].get("commissionAsset"):
                    order["commissionAsset"] = order_trades[0]["commissionAsset"]

        # Sort orders by time (newest first)
        all_orders.sort(key=lambda x: x["time"], reverse=True)
        
        return {
            "total_orders": len(all_orders),
            "period": f"Last {days} days",
            "orders": all_orders
        }
        
    except Exception as e:
        return {"error": str(e)}


