from crewai.tools import tool
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv
import os

load_dotenv()

def get_current_position():
    try:
        position = client.futures_position_information(symbol='BTCUSDT')[0]
        return {
            'positionAmt': position['positionAmt'],
            'entryPrice': position['entryPrice'],
            'unRealizedProfit': position['unRealizedProfit'],
            'leverage': position['leverage']
        }
    except BinanceAPIException as e:
        return f"Error getting position: {str(e)}"



client = Client(
    api_key=os.getenv('BINANCE_API_KEY'),
    api_secret=os.getenv('BINANCE_SECRET_KEY')
)

@tool("Get BTC current position and available balance for new trades from Binance")
def GET_CURRENT_POSITION():
    """Get BTC current position and available balance for new trades from Binance"""
    try:
        # Get account information
        account = client.futures_account()
        
        # Get positions and balance
        positions = account['positions']
        balance = account['totalWalletBalance']
        available_balance = account['availableBalance']
        
        # Find BTC position
        btc_position = next((pos for pos in positions if pos['symbol'] == 'BTCUSDT'), None)
        
        if not btc_position or float(btc_position['positionAmt']) == 0:
            return {
                'position': None,
                'available_balance': float(available_balance),
                'total_balance': float(balance),
            }
            
        position_info = {
            'position': {
                'symbol': btc_position['symbol'],
                'position_side': 'LONG' if float(btc_position['positionAmt']) > 0 else 'SHORT',
                'quantity': abs(float(btc_position['positionAmt'])),
                'entry_price': float(btc_position['entryPrice']),
                'unrealized_pnl': float(btc_position.get('unRealizedPnl', 0)),
                'leverage': int(btc_position.get('leverage', 1))
            },
            'available_balance': float(available_balance),
            'total_balance': float(balance)
        }
            
        return position_info
    except BinanceAPIException as e:
        return f"Error getting position: {str(e)}"

@tool("Execute a trade on Binance futures")
def EXECUTE_TRADE(position_type: str, leverage: int, confidence: float, stop_loss: float, take_profit: float):
    """
    Execute a trade on Binance futures
    
    Args:
        position_type (str): 'LONG' or 'SHORT'
        leverage (int): Leverage amount (10-50)
        confidence (float): Confidence level (0-1)
        stop_loss (float): Stop loss percentage
        take_profit (float): Take profit percentage
    """
    account = client.futures_account()
    usd_amount = float(account['availableBalance'])
    if usd_amount < 100:
        return "Error: Minimum trade amount is 100 USD"
    elif leverage > 50 or leverage < 10:
        return "Error: Leverage must be between 10 and 50"
    else:
        try:
            # Set leverage
            client.futures_change_leverage(symbol='BTCUSDT', leverage=leverage)
            
            # Calculate quantity based on current price
            current_price = float(client.futures_symbol_ticker(symbol='BTCUSDT')['price'])
            quantity = round(usd_amount*leverage*confidence / current_price, 3)
            
            # Execute trade
            if position_type.upper() == 'LONG':
                order = client.futures_create_order(
                    symbol='BTCUSDT',
                    side='BUY',
                    type='MARKET',
                    quantity=quantity,
                    stopPrice=stop_loss,
                    takeProfitPrice=take_profit
                )
            elif position_type.upper() == 'SHORT':
                order = client.futures_create_order(
                    symbol='BTCUSDT',
                    side='SELL',
                    type='MARKET',
                    quantity=quantity,
                    stopPrice=stop_loss,
                    takeProfitPrice=take_profit
                )
            else:
                return "Invalid position type. Use 'LONG' or 'SHORT'"
                
            return f"Trade executed successfully: {order}"
        except BinanceAPIException as e:
            return f"Error executing trade: {str(e)}"

@tool("Close BTC Positions on Binance")
def CLOSE_POSITIONS():
    """Close BTC Positions on Binance"""
    try:
        # Get current position
        position = get_current_position()
        
        # If there's an open position, close it
        if float(position['positionAmt']) != 0:
            # Determine side based on position amount (negative for short, positive for long)
            side = 'SELL' if float(position['positionAmt']) > 0 else 'BUY'
            
            # Close position with market order
            order = client.futures_create_order(
                symbol='BTCUSDT',
                side=side,
                type='MARKET',
                quantity=abs(float(position['positionAmt']))
            )
            return f"Position closed successfully: {order}"
        else:
            return "No open positions to close"
            
    except BinanceAPIException as e:
        return f"Error closing positions: {str(e)}"
