# settings.py
import hashlib

def stable_seed(*parts) -> int:
    """
    Deterministic seed from any number of string-ish parts.
    Example: stable_seed("Nicole", "color")
    """
    joined = "|".join(str(p) for p in parts)
    h = hashlib.sha256(joined.encode("utf-8")).hexdigest()
    # Use first 8 hex chars -> 32-bit int
    return int(h[:8], 16)
