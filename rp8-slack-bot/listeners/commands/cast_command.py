from slack_bolt import Ack, Say, Respond
from slack_sdk import WebClient
from logging import Logger
import time, threading, random
from data import save_data, load_data

def cast_command(ack: Ack, body: dict, client: WebClient, say: Say, respond: Respond, logger: Logger):
    try:
        ack()
        user_id = body["user_id"]

        data = load_data()

        if user_id not in data:
            data[user_id] = {}

        if data[user_id].get("casted"):
            respond("Your line is already cast!")
            return
        
        say(f"<@{user_id}> casted their line...")

        data[user_id]["casted"] = True

        save_data(data)

        def delay_bite():
            time.sleep(5)

            data = load_data()
            user = data.get(user_id, {})

            if not user.get("casted"):
                return
            
            if random.random() > 0.5:
                say(f"A fish is tugging at <@{user_id}>'s line! Use /catch")
            else:
                say(f"A fish is biting for <@{user_id}>! Use /catch")

            time.sleep(3)
            # fish not caught
            say(F"<@{user_id}>'s fish got away!")
            data[user_id]["casted"] = False
            save_data(data)

        threading.Thread(target=delay_bite).start()

    except Exception as e:
        logger.error(e)
