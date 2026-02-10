def interpret_intent(user_input: str):
    user_input = user_input.lower()

    if "cinematic" in user_input:
        return {
            "style": "cinematic",
            "pace": "slow",
            "fps": 8,
            "step": 12
        }

    if "fast" in user_input or "trailer" in user_input:
        return {
            "style": "trailer",
            "pace": "fast",
            "fps": 15,
            "step": 6
        }

    return {
        "style": "reel",
        "pace": "medium",
        "fps": 12,
        "step": 8
    }
