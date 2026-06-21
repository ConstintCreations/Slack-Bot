from slack_bolt import Ack
from slack_sdk import WebClient
from logging import Logger
from data import save_data, load_data, DEFINITIONS

def buy_upgrade_action(ack: Ack, body: dict, client: WebClient, logger: Logger):
    try:
        ack()
        user_id = body["user"]["id"]
        view_id = body["view"]["id"]
        data = load_data()
        user = data[user_id]
        definitions = DEFINITIONS

        upgrade_key, price = body["actions"][0]["value"].split("|")

        owned = user["upgrades"][upgrade_key]
        max = definitions["upgrades"][upgrade_key]["max"]

        bought = False

        if user["money"] >= int(price) and owned <= max:
            user["money"] = user["money"] - int(price)
            user["upgrades"][upgrade_key] = user["upgrades"][upgrade_key] + 1
            bought = True
            save_data(data)

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

        client.views_update(
            view_id=view_id,
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