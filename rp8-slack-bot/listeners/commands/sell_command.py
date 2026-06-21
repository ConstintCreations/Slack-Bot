from slack_bolt import Ack, Say, Respond
from slack_sdk import WebClient
from logging import Logger
import time, threading, random
from data import save_data, load_data

def sell_command(ack: Ack, body: dict, client: WebClient, say: Say, respond: Respond, logger: Logger):
    try:
        ack()
        user_id = body["user_id"]

        data = load_data()

        if len(data[user_id]["inventory"]) == 0:
            respond("It looks like you have nothing to sell. Cast your rod to start fishing!")
            return
        message = "Sold:\n"
        total = 0
        for fish in data[user_id]["inventory"]:
            message += f"    {fish["size"]} {fish["weight"]} lb. [{fish["rarity"]}] {fish["name"]} = ${fish["value"]}\n"
            total += fish["value"]
        message += f"For a total of ${round(total, 1)}! You now have ${data[user_id]["money"] + total}"
        respond(message)

        data[user_id]["money"] = data[user_id]["money"] + total
        data[user_id]["inventory"] = []
        save_data(data)

    except Exception as e:
        logger.error(e)
