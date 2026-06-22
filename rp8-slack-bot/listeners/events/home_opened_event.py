from slack_bolt import Ack
from slack_sdk import WebClient
from logging import Logger
from data import save_data, load_data, DEFINITIONS

def home_opened_event(event, client: WebClient, logger: Logger):
    try:
        user_id = event["user"]
        data = load_data()
        user = data[user_id]
        
        money = user["money"]
        fish_caught = user["fish_caught"]
        best_fish = user["best_fish"]

        fishdex_text = ""

        for rarity in user["fishdex"]:
            fishdex_text += f"\n{rarity}: "
            rarity_caught = 0
            rarity_total = 0
            for caught_fish in user["fishdex"][rarity].values():
                if caught_fish:
                    rarity_caught += 1
                rarity_total += 1
            if rarity != "Secret" or rarity_caught == rarity_total:
                fishdex_text += f"{rarity_caught}/{rarity_total}"
            else:
                fishdex_text += f"{rarity_caught}/?"

        inventory_text = f"{len(user["inventory"])}/{user["upgrades"]["boat_size"]+1}"

        if best_fish:
            best_fish_text = f"{best_fish["size"]} {best_fish["weight"]} lb. [{best_fish["rarity"]}] {best_fish["name"]} (${best_fish["value"]})"
        else:
            best_fish_text = "None"

        client.views_publish(
            user_id=user_id,
            view = {
                "type": "home",
                "blocks": [
                    {"type": "header", "text": {"type": "plain_text", "text": "Fishing Dashboard"}},
                    {"type": "section", "text": {"type": "mrkdwn", "text": f"Money: ${money}\nInventory: {inventory_text}\nFish Caught: {fish_caught}\n"}},
                    {"type": "section", "text": {"type": "mrkdwn", "text": f"\nBest Catch: {best_fish_text}\n"}},
                    {"type": "section", "text": {"type": "mrkdwn", "text": f"\nFishdex: {fishdex_text}"}},
                ]
            }
        )

    except Exception as e:
        logger.error(e)