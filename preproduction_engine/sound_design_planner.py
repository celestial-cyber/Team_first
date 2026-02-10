def plan_sound(intent: dict):
    """Plan sound design from intent."""
    tracks = []
    style = intent.get("style", "reel")
    narration = intent.get("narration", False)
    mood = intent.get("mood")
    
    # Background music track
    if style == "cinematic":
        tracks.append({"name": "background_music", "type": "orchestral", "intensity": "low", "volume_db": -6})
    elif style == "trailer":
        tracks.append({"name": "background_music", "type": "electronic/epic", "intensity": "high", "volume_db": -3})
    else:
        tracks.append({"name": "background_music", "type": "upbeat/pop", "intensity": "medium", "volume_db": -5})
    
    # Narration track
    if narration:
        tracks.append({"name": "narration", "type": "voice_over", "intensity": "focused", "volume_db": 0})
    
    # Sound effects
    tracks.append({"name": "sound_effects", "type": "ambient/sfx", "intensity": "supporting", "volume_db": -12})
    
    if mood:
        tracks.append({"name": f"mood_layer_{mood}", "type": "atmosphere", "intensity": "subtle", "volume_db": -15})
    
    return {"track_count": len(tracks), "style": style, "has_narration": narration, "tracks": tracks}
