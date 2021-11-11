from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import datetime

import requests
import json
from dotenv import load_dotenv

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

load_dotenv()
spreadsheet_id = os.getenv("google_sheet_id")
range_name = os.getenv("prices_range")
secondary_range = os.getenv("time_update_cell")
tertiary_range = os.getenv("gas_price_cell")
etherscan_api_key = os.getenv("etherscan_api_key")


coins = ["bitcoin", "ethereum", "monero", "nano", "polkadot", "loopring",
         "the-graph", "decentraland", "matic-network", "chainlink", "sushi",
         "vechain", "vethor-token", "binancecoin", "havven", "bancor", "uniswap", "algorand",
         "basic-attention-token", "aave", "ethereum-name-service", "cardano", "tornado-cash", "solana", "dogecoin", "maker", "compound-governance-token", "1inch", "defipulse-index", "internet-computer"]

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                range=range_name).execute()
    # values = result.get('values', [])

    values = []
    for x in coins:
        values.append(get_price(x))

    # values.append(get_price("bitcoin")) debugging

    body = {
        "majorDimension": "ROWS",
        'values': values,
        "range": range_name
    }

    # print(values) debugging
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption="RAW", body=body).execute()

    print("Time: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    time_update = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=secondary_range,
        valueInputOption="RAW", body={
            "majorDimension": "ROWS",
            'values': [["Last Updated: " + str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))]],
            "range": secondary_range
        }).execute()


    gas_info = requests.get("https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=" + str(etherscan_api_key)).json()
    gas_price = gas_info["result"]["SafeGasPrice"]

    gas_price_update = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=tertiary_range,
            valueInputOption="RAW", body={
                "majorDimension": "ROWS",
                'values': [["Gas Price: " + str(gas_price) + " Gwei"]],
                "range": tertiary_range
            }).execute()

    print('Prices: {0} cells updated.'.format(result.get('updatedCells')))
    print('Time: {0} cells updated.'.format(time_update.get('updatedCells')))


def get_price(coin):
    r = requests.get("https://api.coingecko.com/api/v3/coins/" + str(coin))
    info = json.loads(r.text)
    print(coin + ": $" + str(info['market_data']['current_price']['usd']))

    return [
        info['market_data']['current_price']['usd'],
        info['market_data']['price_change_24h_in_currency']['usd'],
        info['market_data']['price_change_percentage_24h_in_currency']['usd']/100,
        info['market_data']['market_cap']['usd'],
        info['market_data']['circulating_supply'],
        info['market_data']['total_supply']
    ]


if __name__ == '__main__':
    main()
