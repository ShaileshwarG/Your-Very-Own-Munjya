# query_core_1.py

def query_core_1(user_query):
    user_query = user_query.lower()
    
    # Simulated logic from Core_1
    core_knowledge = {
        "circular reference": "To avoid circular references in Anaplan, use intermediary system modules or staging line items.",
        "timescale mismatch": "Ensure your line item applies the right time scale — model-level, module-level, or line item-specific.",
        "resetting WoS": "Use a SYS Time module to flag quarter start weeks, then build a rolling average that resets each quarter.",
        "supply chain planning": "A strong supply chain planning model includes demand planning, constrained supply logic, and inventory optimization."
    }

    for keyword, response in core_knowledge.items():
        if keyword in user_query:
            return response

    return ""  # triggers fallback
