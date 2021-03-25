from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import requests
import json

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


spreadsheet_id = '18C7kf9PI8_15i9MMfmsUxvLHPIJysZ_6-0ziP8XjAac'
range_name = 'Prices!C2:E21'


coins = ["bitcoin", "ethereum", "monero", "nano", "polkadot", "loopring",
         "the-graph", "decentraland", "matic-network", "chainlink", "sushi",
         "vechain", "vethor-token", "binancecoin", "bancor", "uniswap", "algorand",
         "basic-attention-token", "aave", "cardano"]

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

    # values.append(get_price("bitcoin"))

    body = {
        "majorDimension": "ROWS",
        'values': values,
        "range": range_name
    }
    # print(values)
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption="RAW", body=body).execute()
    print('{0} cells updated.'.format(result.get('updatedCells')))


def get_price(coin):
    r = requests.get("https://api.coingecko.com/api/v3/coins/" + str(coin))
    info = json.loads(r.text)
    print(info['market_data']['price_change_24h_in_currency']['usd'])

    return [
        info['market_data']['current_price']['usd'],
        info['market_data']['price_change_24h_in_currency']['usd'],
        info['market_data']['price_change_percentage_24h_in_currency']['usd']/100,
    ]


if __name__ == '__main__':
    main()
