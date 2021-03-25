# crypto_notifications
Collection of Scripts I wrote to help me track Crypto Prices and investment  profits

## Text Messages
Twilio enabled script that messages me whenever the price goes above or below a certain amount on a major exchange. The idea was inspired by an article that said that Eth dropped to ~$700 on binance from ~$1600 for about 3 minutes. It's set up with heroku deployment so that it uses heroku environment variables.

## Google Sheets
I keep track of all of my various investments on a google sheet but I found that there were no good services to automatically query the price of different assets. There were ones but they had API call limits, lag issues, and general back end failures and couldn't find a good XML service to do it automatically from google sheets, so I did it here.
