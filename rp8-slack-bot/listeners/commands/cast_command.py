from slack_bolt import Ack, Say, Respond
from slack_sdk import WebClient
from logging import Logger
import time, threading, random
from data import save_data, load_data, DEFINITIONS

def cast_command(ack: Ack, body: dict, client: WebClient, say: Say, respond: Respond, logger: Logger):
    try:
        ack()
        user_id = body["user_id"]

        data = load_data()
        user_upgrades = data[user_id]["upgrades"]
        definitions = DEFINITIONS
        upgrades = definitions["upgrades"]

        if data[user_id].get("casted"):
            respond("Your line is already cast!")
            return
        
        if len(data[user_id]["inventory"]) >= user_upgrades["boat_size"] * upgrades["boat_size"]["value_per_upgrade"] + 1:
            respond("It looks like your boat is already full of fish! Sell your haul or increase your boat size to continue casting.")
            return
        
        respond("You cast your line...")

        data[user_id]["casted"] = True

        save_data(data)

        def delay_bite():
            definitions = DEFINITIONS
            upgrades = definitions["upgrades"]
            time.sleep(random.gauss(25 - user_upgrades["average_bite_time"] * upgrades["average_bite_time"]["value_per_upgrade"], (25 - (user_upgrades["average_bite_time"] * upgrades["average_bite_time"]["value_per_upgrade"]))/4))

            data = load_data()
            user = data.get(user_id, {})

            if not user.get("casted"):
                return
            
            data[user_id]["has_bite"] = True
            
            if user_upgrades["autoreel"] > 0:
                definitions = DEFINITIONS
                upgrades = definitions["upgrades"]
                user_rod = definitions["rods"][user["upgrades"]["rod_upgrade"]]
                fish_list = definitions["fish"]
                if random.random() <= user_rod["secret_chance"] + user_upgrades["secret_luck"] * upgrades["secret_luck"]["value_per_upgrade"]:
                    rarity = "Secret"
                else:
                    rarity = random.choices(list(user_rod["chances"].keys()),list(user_rod["chances"].values()), k=1)[0]
                fish_name = random.choice(list(fish_list[rarity].keys()))
                fish = fish_list[rarity][fish_name]

                weight = random.gauss(fish["avg_weight"], fish["avg_weight"]/2) + (fish["avg_weight"] * (user_upgrades["luck"] * upgrades["luck"]["value_per_upgrade"] + user["upgrades"]["rod_upgrade"] * 0.1))
                if weight <= 0.1:
                    weight = 0.1
                round_weight = round(weight, 1)

                proportional_weight = weight/fish["avg_weight"]
                if proportional_weight <= 0.25:
                    fish_size = "Microscopic"
                elif proportional_weight <= 0.5:
                    fish_size = "Tiny"
                elif proportional_weight <= 0.85:
                    fish_size = "Small"
                elif proportional_weight <= 1.15:
                    fish_size = "Average"
                elif proportional_weight <= 1.5:
                    fish_size = "Large"
                elif proportional_weight <= 2:
                    fish_size = "Huge"
                elif proportional_weight <= 3:
                    fish_size = "GIANT"
                elif proportional_weight <= 5:
                    fish_size = "MASSIVE"
                elif proportional_weight <= 7.5:
                    fish_size = "COLOSSAL"
                elif proportional_weight <= 10:
                    fish_size = "BEGEMOTH"
                elif proportional_weight <= 25:
                    fish_size = "LEVIATHAN"
                else:
                    fish_size = "ABYSSAL"

                value = fish["base_value"] + fish["weight_multiplier"]*weight
                value = round(value, 1)

                fish_data = {
                    "rarity": rarity.upper(),
                    "name": fish_name,
                    "size": fish_size,
                    "weight": round_weight,
                    "value": value
                }

                if not(data[user_id]["best_fish"].get("value")) or fish_data["value"] > data[user_id]["best_fish"]["value"]:
                    data[user_id]["best_fish"] = fish_data
                    message = client.chat_postMessage(channel = body["channel_id"], text=f"NEW BEST! <@{user_id}> caught a{"n" if fish_size[0] == 'A' else ""} {fish_size} {round_weight} lb. [{rarity.upper()}] {fish_name}! (${value})")
                    client.reactions_add(channel=body["channel_id"], timestamp=message["ts"], name="trophy")
                else:
                    respond(f"AUTOREEL! You caught a{"n" if fish_size[0] == 'A' else ""} {fish_size} {round_weight} lb. [{rarity.upper()}] {fish_name}! (${value})")

                data[user_id]["inventory"].append(fish_data)
                data[user_id]["fish_caught"] = data[user_id]["fish_caught"] + 1
                data[user_id]["fishdex"][rarity][fish_name] = True

                data[user_id]["casted"] = False
                data[user_id]["has_bite"] = False
                save_data(data)
            else:
                if random.random() > 0.5:
                    respond("A fish is tugging at your line! Reel it in!")
                else:
                    respond("A fish is biting! Reel it in!")
                save_data(data)

                time.sleep(random.gauss(1.5 + user_upgrades["time_to_catch"] * upgrades["time_to_catch"]["value_per_upgrade"], (1.5 + user_upgrades["time_to_catch"] * upgrades["time_to_catch"]["value_per_upgrade"])/8))
                data = load_data()
                if data[user_id]["has_bite"]:
                    respond("The fish got away!")
                    data[user_id]["casted"] = False
                    data[user_id]["has_bite"] = False
                    save_data(data)
                    
            if user_upgrades["autosell"] > 0:
                    if len(data[user_id]["inventory"]) == user_upgrades["boat_size"]+1:
                        message = "AUTOSELL! Sold:\n"
                        total = 0
                        for fish in data[user_id]["inventory"]:
                            message += f"    {fish["size"]} {fish["weight"]} lb. [{fish["rarity"]}] {fish["name"]} = ${fish["value"]}\n"
                            total += fish["value"]
                        total = round(total, 1)
                        message += f"For a total of ${total}! You now have ${data[user_id]["money"] + total}"
                        respond(message)

                        data[user_id]["money"] = data[user_id]["money"] + total
                        data[user_id]["inventory"] = []
            save_data(data)

        threading.Thread(target=delay_bite).start()

    except Exception as e:
        logger.error(e)
