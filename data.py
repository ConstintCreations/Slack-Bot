import json, os

PLAYER_DATA_FILE = "player_data.json"
DEFINITIONS_FILE = "definitions.json"

def _load_data():
    if not os.path.exists(PLAYER_DATA_FILE):
        return {}
    with open(PLAYER_DATA_FILE, "r") as file:
        return json.load(file)
    
def _save_data(data):
    with open(PLAYER_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def load_user(user_id):
    data = _load_data()
    return data.get(user_id)

def save_user(user_id, user_data):
    data = _load_data()
    data[user_id] = user_data
    _save_data(data)

def load_definitions():
    with open(DEFINITIONS_FILE, "r") as file:
        return json.load(file)
    
DEFINITIONS = load_definitions()