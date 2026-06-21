from data import save_data, load_data, DEFINITIONS

def ensure_player_data():
    def middleware(context, body, next, logger):
        user_id = body.get("user_id")

        if not user_id:
            return next()

        data = load_data()
        if user_id not in data:
            base_upgrades = {}
            for name, upgrade in DEFINITIONS["upgrades"].items():
                base_upgrades[name] = upgrade["base_value"]
            base_fishdex = {}
            for rarity, fish_list in DEFINITIONS["fish"].items():
                base_fishdex[rarity] = {}
                for fish_name in fish_list:
                    base_fishdex[rarity][fish_name] = False
            data[user_id] = {
                "cash": 0,
                "inventory": [],
                "upgrades": base_upgrades,
                "fish_caught": 0,
                "best_fish": {},
                "casted": False,
                "has_bite": False,
                "fishdex": base_fishdex
            }

            save_data(data)

        return next()

    return middleware