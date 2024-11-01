from binance import Client
from datetime import datetime, timedelta
from typing import Optional

class BinanceService:
    @staticmethod
    def get_client(api_key: str, api_secret: str) -> Client:
        return Client(api_key, api_secret)

    @staticmethod
    def get_futures_account(api_key: str, api_secret: str):
        client = BinanceService.get_client(api_key, api_secret)
        account_info = client.futures_account()
        account_info["assets"] = [asset for asset in account_info["assets"] if asset["updateTime"] > 0]
        account_info["positions"] = [position for position in account_info["positions"] if float(position["initialMargin"]) > 0]
        return account_info

    @staticmethod
    def change_position_mode(api_key: str, api_secret: str, mode: bool):
        client = BinanceService.get_client(api_key, api_secret)
        return client.futures_change_position_mode(dualSidePosition=mode)

    @staticmethod
    def get_position_mode(api_key: str, api_secret: str):
        client = BinanceService.get_client(api_key, api_secret)
        return client.futures_get_position_mode()

    @staticmethod
    def get_all_orders(api_key: str, api_secret: str, symbol: Optional[str], days: int = 89):
        if days > 90:
            return {
                "error": "Binance only allows fetching orders from the last 90 days",
                "requested_days": days,
                "maximum_days": 90
            }

        client = BinanceService.get_client(api_key, api_secret)
        end_time = int(datetime.now().timestamp() * 1000)
        start_time = int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
        
        all_orders = []
        all_trades = {}
        
        current_end_time = end_time
        while current_end_time > start_time:
            chunk_start_time = max(
                start_time,
                current_end_time - (7 * 24 * 60 * 60 * 1000)
            )
            
            params = {
                "symbol": "BTCUSDT" if not symbol else symbol,
                "startTime": chunk_start_time,
                "endTime": current_end_time,
                "limit": 1000
            }
            
            orders = client.futures_get_all_orders(**params)
            trades = client.futures_account_trades(**params)
            
            for trade in trades:
                order_id = trade["orderId"]
                if order_id not in all_trades:
                    all_trades[order_id] = []
                all_trades[order_id].append(trade)
            
            all_orders.extend(orders)
            current_end_time = chunk_start_time - 1

        for order in all_orders:
            order["timeReadable"] = datetime.fromtimestamp(order["time"] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            if "updateTime" in order:
                order["updateTimeReadable"] = datetime.fromtimestamp(order["updateTime"] / 1000).strftime('%Y-%m-%d %H:%M:%S')
            
            order_trades = all_trades.get(order["orderId"], [])
            if order_trades:
                realized_pnl = sum(float(trade.get("realizedPnl", 0)) for trade in order_trades)
                order["realizedPnl"] = str(realized_pnl)
                
                commission = sum(float(trade.get("commission", 0)) for trade in order_trades)
                order["commission"] = str(commission)
                if order_trades[0].get("commissionAsset"):
                    order["commissionAsset"] = order_trades[0]["commissionAsset"]

        all_orders.sort(key=lambda x: x["time"], reverse=True)
        
        return {
            "total_orders": len(all_orders),
            "period": f"Last {days} days",
            "orders": all_orders
        } 