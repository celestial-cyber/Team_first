def plan_workflow(intent: dict):
    """Create a workflow plan from intent dict."""
    steps = []
    style = intent.get("style", "reel")
    pace = intent.get("pace", "medium")
    mood = intent.get("mood")
    
    if style == "cinematic":
        steps.extend([
            {"phase": 1, "name": "color grading", "priority": "high", "notes": "slow cinematic look"},
            {"phase": 2, "name": "slow dissolves", "priority": "high", "notes": "smooth transitions"},
            {"phase": 3, "name": "music sync", "priority": "medium", "notes": "ambient/orchestral"}
        ])
    elif style == "trailer":
        steps.extend([
            {"phase": 1, "name": "sharp cuts", "priority": "high", "notes": "fast pacing"},
            {"phase": 2, "name": "color boost", "priority": "high", "notes": "vibrant, contrasty"},
            {"phase": 3, "name": "sound effects", "priority": "medium", "notes": "punchy, energetic"}
        ])
    else:
        steps.extend([
            {"phase": 1, "name": "quick loops", "priority": "high", "notes": "Instagram-friendly"},
            {"phase": 2, "name": "trending audio", "priority": "medium", "notes": "upbeat soundtrack"},
            {"phase": 3, "name": "hashtags setup", "priority": "low", "notes": "distribution ready"}
        ])
    
    if mood:
        steps.append({"phase": 4, "name": f"mood: {mood}", "priority": "medium", "notes": f"apply {mood} tone"})
    
    return {"style": style, "pace": pace, "total_steps": len(steps), "steps": steps}
