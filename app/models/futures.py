from typing import List, Optional
from pydantic import BaseModel

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
                "totalInitialMargin": "29.02453367",
                "totalMaintMargin": "0.58049067",
                "totalWalletBalance": "8459.32092583",
                "totalUnrealizedProfit": "0.83706839",
                "totalMarginBalance": "8460.15799422",
                "totalPositionInitialMargin": "29.02453367",
                "totalOpenOrderInitialMargin": "0.00000000",
                "totalCrossWalletBalance": "8459.32092583",
                "totalCrossUnPnl": "0.83706839",
                "availableBalance": "8431.13099216",
                "maxWithdrawAmount": "8431.13099216",
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
                        "unrealizedProfit": "0.83706839",
                        "marginBalance": "8460.15799422",
                        "maintMargin": "0.58049067",
                        "initialMargin": "29.02453367",
                        "positionInitialMargin": "29.02453367",
                        "openOrderInitialMargin": "0.00000000",
                        "maxWithdrawAmount": "8431.13099216",
                        "crossWalletBalance": "8459.32092583",
                        "crossUnPnl": "0.83706839",
                        "availableBalance": "8431.13099216",
                        "marginAvailable": True,
                        "updateTime": 1729518843031
                    }
                ],
                "positions": [
                    {
                        "symbol": "BTCUSDT",
                        "initialMargin": "29.02453367",
                        "maintMargin": "0.58049067",
                        "unrealizedProfit": "0.83706839",
                        "positionInitialMargin": "29.02453367",
                        "openOrderInitialMargin": "0",
                        "leverage": "5",
                        "isolated": False,
                        "entryPrice": "72142.8",
                        "breakEvenPrice": "72175.26426",
                        "maxNotional": "480000000",
                        "positionSide": "LONG",
                        "positionAmt": "0.002",
                        "notional": "145.12266839",
                        "isolatedWallet": "0",
                        "updateTime": 1730318811018,
                        "bidNotional": "0",
                        "askNotional": "0"
                    }
                ]
            }
        } 

class FuturesOrder(BaseModel):
    orderId: int
    symbol: str
    status: str
    clientOrderId: str
    price: str
    avgPrice: str
    origQty: str
    executedQty: str
    cumQuote: str
    timeInForce: str
    type: str
    reduceOnly: bool
    closePosition: bool
    side: str
    positionSide: str
    stopPrice: str
    workingType: str
    priceMatch: str
    selfTradePreventionMode: str
    goodTillDate: int
    priceProtect: bool
    origType: str
    time: int
    updateTime: int
    timeReadable: str
    updateTimeReadable: str
    realizedPnl: str
    commission: str
    commissionAsset: str

class FuturesOrdersResponse(BaseModel):
    total_orders: int
    period: str
    orders: List[FuturesOrder]

    class Config:
        json_schema_extra = {
            "example": {
                "total_orders": 2,
                "period": "Last 90 days",
                "orders": [
                    {
                        "orderId": 457353370213,
                        "symbol": "BTCUSDT",
                        "status": "FILLED",
                        "clientOrderId": "web_FWuB39lSCfxMzlz5CvpD",
                        "price": "0",
                        "avgPrice": "72142.80000",
                        "origQty": "0.002",
                        "executedQty": "0.002",
                        "cumQuote": "144.28560",
                        "timeInForce": "GTC",
                        "type": "MARKET",
                        "reduceOnly": False,
                        "closePosition": False,
                        "side": "BUY",
                        "positionSide": "LONG",
                        "stopPrice": "0",
                        "workingType": "CONTRACT_PRICE",
                        "priceMatch": "NONE",
                        "selfTradePreventionMode": "NONE",
                        "goodTillDate": 0,
                        "priceProtect": False,
                        "origType": "MARKET",
                        "time": 1730318811018,
                        "updateTime": 1730318811018,
                        "timeReadable": "2024-10-31 03:06:51",
                        "updateTimeReadable": "2024-10-31 03:06:51",
                        "realizedPnl": "0.0",
                        "commission": "0.00010858",
                        "commissionAsset": "BNB"
                    },
                    {
                        "orderId": 448703081806,
                        "symbol": "BTCUSDT",
                        "status": "FILLED",
                        "clientOrderId": "android_rk96gtcfnFbeDOiV6tIz",
                        "price": "0",
                        "avgPrice": "67300.10000",
                        "origQty": "0.200",
                        "executedQty": "0.200",
                        "cumQuote": "13460.02000",
                        "timeInForce": "GTC",
                        "type": "MARKET",
                        "reduceOnly": True,
                        "closePosition": True,
                        "side": "SELL",
                        "positionSide": "LONG",
                        "stopPrice": "67300",
                        "workingType": "MARK_PRICE",
                        "priceMatch": "NONE",
                        "selfTradePreventionMode": "NONE",
                        "goodTillDate": 0,
                        "priceProtect": True,
                        "origType": "STOP_MARKET",
                        "time": 1729511207953,
                        "updateTime": 1729518843031,
                        "timeReadable": "2024-10-21 18:46:47",
                        "updateTimeReadable": "2024-10-21 20:54:03",
                        "realizedPnl": "43.52",
                        "commission": "0.01016608",
                        "commissionAsset": "BNB"
                    }
                ]
            }
        } 