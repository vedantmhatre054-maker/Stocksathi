import spacy
import re

nlp = spacy.load("en_core_web_sm")

def process_message(text):
    # 🔥 FIX: split 5kg → 5 kg
    text = re.sub(r'(\d+)([a-zA-Z]+)', r'\1 \2', text)

    # 🔥 MULTI-INTENT SPLIT
    parts = text.split("aur")

    results = []

    for part in parts:
        doc = nlp(part.lower())

        quantity = None
        item = None
        action = None
        unit = "kg"

        # 🔹 quantity
        for token in doc:
            if token.like_num:
                try:
                    quantity = int(token.text)
                except:
                    pass

        # 🔹 action detection
        add_words = ["aaya", "aale", "added", "aayi"]
        remove_words = ["gaya", "gele", "sold"]

        for token in doc:
            if token.text in remove_words:
                action = "remove"
            elif token.text in add_words:
                action = "add"

        # 🔹 item detection (GENERIC)
        ignore_words = set([
            "kg", "packet", "litre",
            "aaya", "aale", "gaya", "gele",
            "bhai", "aaj", "kal", "tha", "aur"
        ])

        for token in doc:
            if (
                not token.like_num and
                token.text not in ignore_words and
                token.is_alpha
            ):
                item = token.text
                break

        # 🔥 append valid only
        if item and quantity and action:
            results.append({
                "item": item,
                "quantity": quantity,
                "unit": unit,
                "action": action
            })

    return results