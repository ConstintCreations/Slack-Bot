from slack_bolt import Ack, Say, Respond
from slack_sdk import WebClient
from logging import Logger
import time, threading, random
from data import save_user, load_user

def sell_command(ack: Ack, body: dict, client: WebClient, say: Say, respond: Respond, logger: Logger):
    try:
        ack()
        user_id = body["user_id"]

        user = load_user(user_id)


        if len(user["inventory"]) == 0:
            respond("It looks like you have nothing to sell. Cast your rod to start fishing!")
            return
        message = "Sold:\n"
        total = 0
        for fish in user["inventory"]:
            message += f"    {fish["size"]} {fish["weight"]} lb. [{fish["rarity"]}] {fish["name"]} = ${fish["value"]}\n"
            total += fish["value"]
        total = round(total, 1)
        message += f"For a total of ${total}! You now have ${user["money"] + total}"
        respond(message)

        user["money"] = user["money"] + total
        user["inventory"] = []
        save_user(user_id, user)

    except Exception as e:
        logger.error(e)
