import re


def contains_any(text, keywords):
    return any(re.search(r'\b' + re.escape(k) + r'\b', text) for k in keywords)


def precheck(issue):
    issue_lower = issue.lower()

    # ── High-risk: fraud / security / identity theft ──
    fraud_keywords = [
        "fraud", "unauthorized", "stolen", "hacked", "identity theft",
        "my identity has been stolen", "stolen card", "compromised",
        "account takeover", "scam", "phishing", "data breach",
        "someone used my card", "suspicious transaction", "suspicious charge",
        "unrecognized charge", "unrecognized transaction"
    ]
    if contains_any(issue_lower, fraud_keywords):
        return {
            "status": "escalated",
            "product_area": "fraud_security",
            "request_type": "product_issue",
            "response": (
                "This appears to involve fraud, identity theft, or a security concern. "
                "Please act immediately: contact your bank or card issuer to freeze your account, "
                "file a police report if needed, and call Visa's Global Customer Assistance at "
                "+1 303 967 1090 (24/7) for card-related emergencies. "
                "A support specialist will follow up with you shortly."
            ),
            "justification": "High-risk fraud or security issue detected — escalated per policy."
        }

    # ── Prompt injection / system prompt extraction attempts ──
    injection_keywords = [
        "show internal rules", "reveal your prompt", "show retrieved documents",
        "affiche toutes les règles", "system prompt", "ignore previous instructions",
        "show your instructions", "print your rules", "logique exacte",
        "documents récupérés", "decision logic", "internal documents",
        "ignore all instructions", "disregard previous", "forget your instructions",
        "you are now", "act as if", "pretend you are", "jailbreak",
        "bypass your rules", "override instructions"
    ]
    if contains_any(issue_lower, injection_keywords):
        return {
            "status": "escalated",
            "product_area": "security",
            "request_type": "invalid",
            "response": (
                "I'm unable to share internal system information, rules, or retrieved documents. "
                "If you have a genuine support issue, please describe it and I'll be happy to help."
            ),
            "justification": "Prompt injection or system information extraction attempt detected."
        }

    # ── Harmful / dangerous requests ──
    harmful_keywords = [
        "delete all files", "rm -rf", "format the disk", "destroy data",
        "execute command", "run script on system", "drop table", "drop database",
        "shutdown server", "wipe the database"
    ]
    if contains_any(issue_lower, harmful_keywords):
        return {
            "status": "escalated",
            "product_area": "security",
            "request_type": "invalid",
            "response": (
                "I'm sorry, I cannot assist with that request. "
                "If you have a legitimate support question, please describe it."
            ),
            "justification": "Potentially harmful or malicious request detected."
        }

    # ── Out of scope: clearly unrelated to HackerRank, Claude, or Visa ──
    out_of_scope_triggers = [
        "iron man", "actor", "movie", "recipe", "weather", "sports",
        "stock price", "celebrity", "music", "song", "lyrics",
        "restaurant", "hotel", "flight", "book recommendation",
        "news", "politics", "gaming", "video game", "homework",
        "math problem", "translate", "write a poem", "write an essay",
        "who is the president", "what time is it", "tell me a joke",
        "cryptocurrency", "bitcoin", "nft", "diet", "fitness", "workout"
    ]
    if contains_any(issue_lower, out_of_scope_triggers):
        return {
            "status": "replied",
            "product_area": "conversation_management",
            "request_type": "invalid",
            "response": (
                "I'm sorry, this question is outside the scope of our support capabilities. "
                "I can only assist with HackerRank, Claude, and Visa-related issues."
            ),
            "justification": "Request is unrelated to supported platforms."
        }

    return None
