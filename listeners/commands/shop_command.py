from slack_bolt import Ack, Say, Respond
from slack_sdk import WebClient
from logging import Logger
import time, threading, random
from data import save_user, load_user, DEFINITIONS

def shop_command(ack: Ack, body: dict, client: WebClient, say: Say, respond: Respond, logger: Logger):
    try:
        ack()
        user_id = body["user_id"]
        user = load_user(user_id)
        definitions = DEFINITIONS

        blocks = []

        money_block = {"type": "section", "text": {"type": "mrkdwn", "text": f"Money: ${user['money']}"}}
        blocks.append(money_block)

        for key, upgrade in definitions["upgrades"].items():
            current_value = user["upgrades"][key]
            price = int(upgrade["base_price"] * (upgrade["price_multiplier"] ** current_value))
            show_price = not(current_value == upgrade['max'])
            price_text = f" | ${price}" if show_price else ''
            upgrade_block = {"type": "section", "text": {"type": "mrkdwn", "text": f"{upgrade['name']} - {upgrade['description']}\nOwned {current_value}/{upgrade['max']}{price_text}"}, "accessory": {"type": "button", "text": {"type": "plain_text", "text": "Buy"}, "value": f"{key}|{price}", "action_id": "buy_upgrade"}}
            blocks.append({"type": "divider"})
            blocks.append(upgrade_block)

        client.views_open(
            trigger_id=body["trigger_id"],
            view={
                "type": "modal",
                "callback_id": "shop_modal",
                "title": {"type": "plain_text", "text": "Fishing Shop"},
                "blocks": blocks
            }
        )

    except Exception as e:
        logger.error(e)
