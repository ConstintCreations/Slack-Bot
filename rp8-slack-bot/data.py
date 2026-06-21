import json, os

PLAYER_DATA_FILE = "player_data.json"
DEFINITIONS_FILE = "definitions.json"

def load_data():
    if not os.path.exists(PLAYER_DATA_FILE):
        return {}
    with open(PLAYER_DATA_FILE, "r") as file:
        return json.load(file)
    
def save_data(data):
    with open(PLAYER_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def load_definitions():
    with open(DEFINITIONS_FILE, "r") as file:
        return json.load(file)
    
DEFINITIONS = load_definitions()