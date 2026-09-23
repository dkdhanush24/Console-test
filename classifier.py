"""
classifier.py
-------------
Keyword-based issue categorisation and priority detection.
No machine learning is used in Sprint 1.
"""


# ---------------------------------------------------------------------------
# Category definitions: category_name -> list of keywords
# ---------------------------------------------------------------------------
CATEGORIES = {
    "WiFi Connectivity": [
        "wifi", "wi-fi", "internet", "network", "connectivity",
        "connection", "connecting", "router", "hotspot", "ethernet",
        "bandwidth", "signal", "ping", "dns",
    ],
    "Password/Login": [
        "password", "login", "sign in", "signin", "log in", "credentials",
        "authentication", "access", "locked", "account", "username",
        "forgot password", "reset password",
    ],
    "Email Problem": [
        "email", "e-mail", "outlook", "mail", "inbox", "smtp",
        "imap", "calendar", "meeting invite", "attachment",
    ],
    "Printer Problem": [
        "printer", "printing", "print", "scanner", "scan",
        "paper jam", "ink", "toner", "spooler",
    ],
    "Software Problem": [
        "software", "application", "app", "crash", "crashing",
        "install", "installation", "update", "upgrade", "error",
        "not responding", "freeze", "freezing", "bug", "virus",
        "antivirus", "malware",
    ],
    "Hardware Problem": [
        "laptop", "desktop", "keyboard", "mouse", "screen",
        "monitor", "display", "battery", "charger", "usb",
        "port", "speaker", "audio", "headphone", "webcam",
        "camera", "hard drive", "ssd", "ram", "memory",
    ],
}

# ---------------------------------------------------------------------------
# Priority rules: priority_name -> list of trigger keywords
# ---------------------------------------------------------------------------
PRIORITY_RULES = {
    "High": [
        "server", "system down", "cannot work", "critical",
        "security", "breach", "hacked", "ransomware", "down",
        "outage", "urgent", "emergency", "data loss",
    ],
    "Medium": [
        "wifi", "email", "printer", "software", "application",
        "app", "network", "internet", "connection", "outlook",
        "password", "login",
    ],
    "Low": [
        "mouse", "keyboard", "slow", "display", "screen",
        "monitor", "battery", "speaker", "audio", "webcam",
        "minor", "small", "occasionally",
    ],
}


def classify_issue(description: str) -> dict:
    """
    Analyse *description* with keyword matching and return a dict:
        {
            "category":          str,
            "detected_keywords": list[str],
            "priority":          str,
        }
    """
    text = description.lower()

    # ── Category detection ──────────────────────────────────────────────────
    best_category = "Unknown"
    best_count = 0
    all_detected = []

    for category, keywords in CATEGORIES.items():
        matched = [kw for kw in keywords if kw in text]
        if len(matched) > best_count:
            best_count = len(matched)
            best_category = category
            all_detected = matched

    # ── Priority detection ──────────────────────────────────────────────────
    priority = _detect_priority(text)

    return {
        "category": best_category,
        "detected_keywords": all_detected,
        "priority": priority,
    }


def _detect_priority(text: str) -> str:
    """
    Apply priority rules in order High -> Medium -> Low.
    Default is Medium if nothing matches.
    """
    for level in ("High", "Medium", "Low"):
        for kw in PRIORITY_RULES[level]:
            if kw in text:
                return level
    return "Medium"
