# IStoBot
Helps you to be 100% aware of your stock with multiple tools:
* Alert mechanism.
* Stock information from any source.
* Act and notify on specific scenarios.

# API
API sources we used to analyse the stock.
Target is to make `symbol` component generic as possible to let users add APIs as many they want.
# bot
Contain all non-user needed actions.
Inside bot, we'll find:
## Flows
We can create scenarios and act upon them; Alert via SMS, Suggest buying symbol and more ...
## Alerts
Alerts we want to use: SMS, Email and more ...
## Filters
During flow writing we filter unwanted companies by logic.
Filter target is to get only relevant symbols and it'll do that by:
* Screener
* News
* User custom choice

Those filters can get through JSON file input.
## Logics
Each code logic found in this folder.
We'll use them during symbol Flows and more ...
# Component
## Symbol
Should be accessible to all project's code functionalities.
Here we get access to any APIs we'll want.
## Server
If we want to create system that based on those logics we need server to parse our requests.
