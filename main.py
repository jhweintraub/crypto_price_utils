import requests
from dotenv import load_dotenv
import os
from coinbase.wallet.client import Client as CoinbaseClient
from binance.client import Client as binanceClient
from twilio.rest import Client as twilioClient


def get_coinbase_price():
    coinbase_key = os.getenv("coinbase_api_key")
    coinbase_secret = os.getenv("coinbase_api_secret")
    client = CoinbaseClient(coinbase_key, coinbase_secret)

    ether_price = client.get_buy_price(currency_pair='ETH-USD').amount
    return {"exchange": "Coinbase", "price": float(ether_price)}

def get_binance_price():
    binance_key = os.getenv("binance_api_key")
    binance_secret = os.getenv("binance_api_secret")
    client = binanceClient(binance_key, binance_secret)
    ether_price = client.get_symbol_ticker(symbol="ETHUSDT")
    return {"exchange": "Binance", "price": float(ether_price['price'])}


def send_price_alert(exchange, price, isDrop):
    # Your Account SID from twilio.com/console
    account_sid = os.getenv("twilio_account_sid")
    # Your Auth Token from twilio.com/console
    auth_token = os.getenv("twilio_auth_token")

    client = twilioClient(account_sid, auth_token)

    if isDrop:
        message = "Ether Price has dropped to $" + str(price) + " on " + exchange + "!"
    else:
        message = "Ether Price has risen to $" + str(price) + " on " + exchange + "!"

    alert = client.messages.create(
        to=os.getenv("your_number"),
        from_=os.getenv("twilio_phone_number"),
        body=message)

def main():
    load_dotenv()

    low_alert_amount = float(os.getenv("low_alert_amount"))
    high_alert_amount = float(os.getenv("high_alert_amount"))

    prices = []
    get_binance_price()
    prices.append(get_coinbase_price())
    prices.append(get_binance_price())
    print(prices)

    for x in prices:
        if(x["price"]) > low_alert_amount:
            # send_price_alert(x["exchange"], x["price"], True)
            print("this is a test")
            os.environ['low_alert_amount'] = str(low_alert_amount - 100)
            # print(float(os.getenv("low_alert_amount")))
            # so you don't get spammed by every exchange but do get alerted by sudden crashed
            break

        if (x["price"]) > high_alert_amount:
            send_price_alert(x["exchange"], x["price"], False)
            os.environ['high_alert_amount'] = str(high_alert_amount + 100)
            break

main()
