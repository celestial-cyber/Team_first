import os
import json
import requests

#!
def request_intent_from_llm(prompt: str, timeout: int = 30):
    """Send the user's prompt to an external LLM endpoint and return a parsed intent dict.

    Expects environment variables:
      - LLM_API_URL
      - LLM_API_KEY (optional, Bearer)

    The API is expected to return JSON containing a top-level `intent` object or
    a direct mapping of keys. If not available or on error, returns None.
    """
    api_url = os.environ.get("LLM_API_URL")
    api_key = os.environ.get("LLM_API_KEY")
    if not api_url:
        return None

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {"prompt": prompt}
    try:
        r = requests.post(api_url, headers=headers, json=payload, timeout=timeout)
        if r.status_code != 200:
            print(f"[LLM CLIENT] LLM request failed: {r.status_code} {r.text}")
            return None
        data = r.json()
    except Exception as e:
        print(f"[LLM CLIENT] Request error: {e}")
        return None

    # Accept responses like {"intent": {...}} or directly {...}
    if isinstance(data, dict):
        if "intent" in data and isinstance(data["intent"], dict):
            return data["intent"]
        # otherwise assume the payload itself is the intent map
        return data

    return None
