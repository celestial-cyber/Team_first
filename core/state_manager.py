import json
import os

def save_state(state: dict, states_dir: str, name: str = "state_1.json"):
    os.makedirs(states_dir, exist_ok=True)
    with open(os.path.join(states_dir, name), "w") as f:
        json.dump(state, f, indent=2)
