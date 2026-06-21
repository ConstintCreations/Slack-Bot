from slack_bolt import Ack, Say, Respond
from slack_sdk import WebClient
from logging import Logger
import time, threading, random
from data import save_data, load_data

def fishdex_command(ack: Ack, body: dict, client: WebClient, say: Say, respond: Respond, logger: Logger):
    try:
        ack()
        user_id = body["user_id"]
        data = load_data()

        text = body["text"].strip()
        if text == "":
            target_user_id = user_id
        else:
            text = text.lstrip("@")
            for user, values in data.items():
                if values["username"].lower() == text.lower():
                    target_user_id = user
                    break
            else:
                respond("User could not be found or has not played.")
                return
        all_rarities = ["Common", "Uncommon", "Rare", "Epic", "Legendary", "Secret"]

        fish = data[target_user_id]["best_fish"]

        fish_found_count = 0
        total_count = 0
        for rarity in all_rarities:
            for _, value in data[target_user_id]["fishdex"][rarity].items():
                if value:
                    fish_found_count += 1
                total_count += 1

        secret_fish_found = {}
        total_secret_fish = 0
        for secret_fish, value in data[target_user_id]["fishdex"]["Secret"].items():
            if value:
                secret_fish_found[secret_fish] = value
            total_secret_fish += 1

        if len(secret_fish_found) == total_secret_fish:
            all_secret_fish_found = True
        else:
            all_secret_fish_found = False

        message = f"{"Your" if target_user_id == user_id else f"{data[target_user_id]["username"]}'s"} Fishdex:\n\nBest Catch: {f"{fish["size"]} {fish["weight"]} lb. [{fish["rarity"]}] {fish["name"]} (${fish["value"]})" if fish else "None"}\nFish Caught: {data[target_user_id]["fish_caught"]}\n"

        if all_secret_fish_found:
            message += f"Fish Found: {fish_found_count}/{total_count}\n"
        else:
            message += f"Fish Found: {fish_found_count}/{total_count-total_secret_fish + len(secret_fish_found)}?\n\n"

        for rarity in all_rarities:
            message += f"{rarity}:\n"
            if rarity != "Secret" or all_secret_fish_found:
                for fish, value in data[target_user_id]["fishdex"][rarity].items():
                    message += f"   {fish} - {"CAUGHT" if value else "UNCAUGHT"}\n"
            else:
                for fish, value in secret_fish_found.items():
                    message += f"   {fish} - {"CAUGHT" if value else "UNCAUGHT"}\n"
                message += "   ???"

        respond(message)

    except Exception as e:
        logger.error(e)
