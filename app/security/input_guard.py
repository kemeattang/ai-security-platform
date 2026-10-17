SUSPICIOUS_PATTERNS = ["ignore previous instructions", "ignore all previous instructions", "reveal system prompt", "show system prompt"]

def inspect_prompt(prompt: str) -> dict:
    normalized = prompt.lower().strip()
    for pattern in SUSPICIOUS_PATTERNS:
        if pattern in normalized:
            return {"allowed": False, "risk": "prompt_injection", "reason": f"suspicious pattern detected: {pattern}"}
    return {"allowed": True, "risk": None, "reason": "no known suspicious pattern detected"}
