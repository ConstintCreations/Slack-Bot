from slack_bolt import Ack, Say, Respond
from slack_sdk import WebClient
from logging import Logger
import time, threading, random
from data import save_user, load_user, DEFINITIONS

def reel_command(ack: Ack, body: dict, client: WebClient, say: Say, respond: Respond, logger: Logger):
    try:
        ack()
        user_id = body["user_id"]

        user = load_user(user_id)
        user_upgrades = user["upgrades"]

        if user.get("casted") and user["has_bite"]:

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

            if not(user["best_fish"].get("value")) or fish_data["value"] > user["best_fish"]["value"]:
                user["best_fish"] = fish_data
                message = client.chat_postMessage(channel = body["channel_id"], text=f"NEW BEST! <@{user_id}> caught a{"n" if fish_size[0] == 'A' else ""} {fish_size} {round_weight} lb. [{rarity.upper()}] {fish_name}! (${value})")
                client.reactions_add(channel=body["channel_id"], timestamp=message["ts"], name="trophy")
            else:
                respond(f"You caught a{"n" if fish_size[0] == 'A' else ""} {fish_size} {round_weight} lb. [{rarity.upper()}] {fish_name}! (${value})")

            user["inventory"].append(fish_data)
            user["fish_caught"] = user["fish_caught"] + 1
            user["fishdex"][rarity][fish_name] = True

            user["casted"] = False
            user["has_bite"] = False

            if user_upgrades["autosell"] > 0:
                if len(user["inventory"]) == user_upgrades["boat_size"]+1:
                    message = "AUTOSELL! Sold:\n"
                    total = 0
                    for fish in user["inventory"]:
                        message += f"    {fish["size"]} {fish["weight"]} lb. [{fish["rarity"]}] {fish["name"]} = ${fish["value"]}\n"
                        total += fish["value"]
                    total = round(total, 1)
                    message += f"For a total of ${total}! You now have ${user["money"] + total}"
                    respond(message)

                    user["money"] = user["money"] + total
                    user["inventory"] = []

        elif user.get("casted"):
            respond("Oops! it looks like you reeled in too early! Wait for a bite before you reel in.")
            user["casted"] = False
        else:
            respond("You need to cast your rod first!")

        save_user(user_id, user)
        return

    except Exception as e:
        logger.error(e)
