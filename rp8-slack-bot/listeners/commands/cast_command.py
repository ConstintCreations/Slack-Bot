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

        if data[user_id].get("casted"):
            respond("Your line is already cast!")
            return
        
        if len(data[user_id]["inventory"]) >= data[user_id]["upgrades"]["boat_size"]:
            respond("It looks like your boat is already full of fish! Sell your haul or increase your boat size to continue casting.")
            return
        
        respond("You cast your line...")

        data[user_id]["casted"] = True

        save_data(data)

        def delay_bite():
            time.sleep(random.gauss(5, 1))

            data = load_data()
            user = data.get(user_id, {})

            if not user.get("casted"):
                return
            
            if random.random() > 0.5:
                respond("A fish is tugging at your line! Reel it in!")
            else:
                respond("A fish is biting! Reel it in!")
            data[user_id]["has_bite"] = True
            save_data(data)

            time.sleep(3)
            data = load_data()
            if data[user_id]["has_bite"]:
                respond("The fish got away!")
                data[user_id]["casted"] = False
                data[user_id]["has_bite"] = False
                save_data(data)

        threading.Thread(target=delay_bite).start()

    except Exception as e:
        logger.error(e)
