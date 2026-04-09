def parse_message(text):
    text = text.lower()
    words = text.split()

    quantity = None
    unit = None
    item = None
    action = None

    # 🔹 Quantity
    for word in words:
        if word.isdigit():
            quantity = int(word)

    # 🔹 Units (multi-language)
    units_map = {
        "kg": "kg",
        "kilo": "kg",
        "kilos": "kg",
        "killo": "kg",
        "packet": "packet",
        "pack": "packet",
        "pkt": "packet",
        "litre": "litre",
        "liter": "litre"
    }

    for word in words:
        if word in units_map:
            unit = units_map[word]

    # 🔥 ACTION (HINDI + MARATHI + ROMAN 🔥)
    add_words = [
        "aaya", "aya", "added",
        "aala", "aali", "aale",   # Marathi
        "aayi", "aaye" ,"ALE"           # Hindi variants
    ]

    remove_words = [
        "gaya", "geli", "gele",   # Marathi
        "becha", "sold",
        "gayi", "gaye","GELE"
    ]

    # 🔥 FIRST CHECK REMOVE (IMPORTANT)
    for word in words:
        if word in remove_words:
            action = "remove"
            break

    # 🔥 THEN CHECK ADD
    if not action:
        for word in words:
            if word in add_words:
                action = "add"
                break

   
    # 🔥 AUTO ITEM DETECTION (GENERIC)
    ignore_words = set(units_map.keys()) | set(add_words) | set(remove_words)

    for word in words:
        if not word.isdigit() and word not in ignore_words:
            item = word
            break

    return {
        "item": item,
        "quantity": quantity,
        "unit": unit,
        "action": action
    }