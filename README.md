# Slack Bot Fishing Game

Fishing Game is a Slack-based incremental fishing game where players cast, reel, and sell fish to buy upgrades that help them complete their Fishdex.

![Screenshot](/assets/slack_bot_fishing_game.png)

## Commands
- /cast | Casts your rod
- /reel | Reels in your rod
- /sell | Sells your fish
- /shop | Opens the shop
- /fishdex [User] | See what fish you, or another user have caught

## Features
- Catchable fish of different rarities and randomized sizes
- Fishing Dashboard on the app's homepage
- Shop modal with various upgrades from increased luck to automatically selling fish
- Fishdex that shows all the fish you have caught or are yet to catch
- Keeps track of your best catch, and broadcasts any new best catches you have in the channel

## Local Usage
If you want to run this app locally, you will need to install it to your own workspace with `slack create` and `slack run`