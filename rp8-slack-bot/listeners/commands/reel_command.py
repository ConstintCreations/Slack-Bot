from slack_bolt import Ack, Say, Respond
from slack_sdk import WebClient
from logging import Logger
import time, threading, random
from data import save_data, load_data

def reel_command(ack: Ack, body: dict, client: WebClient, say: Say, respond: Respond, logger: Logger):
    try:
        ack()
        user_id = body["user_id"]
        data = load_data()

        if user_id not in data:
            data[user_id] = {}

        if data[user_id].get("casted") and data[user_id]["has_bite"]:
            say(f"<@{user_id}> caught a fish!")
            data[user_id]["casted"] = False
            data[user_id]["has_bite"] = False
        elif data[user_id].get("casted"):
            respond("Oops! it looks like you reeled in too early! Wait for a bite before you reel in.")
            data[user_id]["casted"] = False
        else:
            respond("You need to cast your rod first!")

        save_data(data)
        return

    except Exception as e:
        logger.error(e)
