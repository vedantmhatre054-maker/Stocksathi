from email import message

from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from nlp_engine import process_message
from mongo_db import update_stock, get_stock


app = FastAPI()

# Create DB table on start



@app.get("/")
def home():
    return {"message": "Server working ✅"}


@app.post("/webhook")
async def webhook(
    Body: str = Form(...),
    From: str = Form(...)
):
    message = Body.lower()

    # 🔥 QUERY DETECTION
    if "kitna" in message or "stock" in message:
        words = message.split()

        item = None
        for word in words:
            if word not in ["kitna", "hai", "stock"]:
                item = word
                break

        qty, unit = get_stock(item)

        if qty is not None:
            reply = f"📦 {item}: {qty} {unit}"

            # ⚠️ Low stock alert (already correct)
            if qty < 5:
                reply += "\n⚠️ Low stock! Order soon"
        else:
            reply = f"❌ {item} not found"

        return PlainTextResponse(reply)

    # 🔥 UPDATE FLOW
    parsed_list = process_message(message)

    reply = ""

    for parsed in parsed_list:
        item = parsed.get("item")
        quantity = parsed.get("quantity")
        unit = parsed.get("unit")
        action = parsed.get("action")

        if not item or not quantity or not action:
            continue

        new_qty = update_stock(item, quantity, unit, action)

        reply += f"✅ {item}: now {new_qty} {unit}\n"

        if new_qty == 0:
            reply += "🚨 Out of stock!\n"
        elif new_qty < 5:
            reply += "⚠️ Low stock! Order soon\n"

    # ❌ If nothing valid parsed
    if not reply:
        return PlainTextResponse("❌ Samajh nahi aaya, sahi format bhejo")

    return PlainTextResponse(reply)