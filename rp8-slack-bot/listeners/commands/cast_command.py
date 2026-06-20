from slack_bolt import Ack, Respond
from slack_sdk import WebClient
from logging import Logger
import time, threading, random

def cast_command(ack: Ack, body: dict, client: WebClient, respond: Respond, logger: Logger):
    try:
        ack()
        user_id = body["user_id"]
        respond(f"<@{user_id}> casted their line...")

        def delay_bite():
            time.sleep(20)
            
            if random.random() > 0.5:
                respond(f"A fish is tugging at <@{user_id}>'s line!")
            else:
                respond(f"A fish is biting for <@{user_id}>!")

        threading.Thread(target=delay_bite).start()

    except Exception as e:
        logger.error(e)
