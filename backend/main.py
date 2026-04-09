from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from parser import parse_message
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
    parsed = parse_message(message)

    item = parsed.get("item")
    quantity = parsed.get("quantity")
    unit = parsed.get("unit")
    action = parsed.get("action")

    # ❌ Invalid input handling
    if not item or not quantity or not action:
        return PlainTextResponse("❌ Samajh nahi aaya, sahi format bhejo")

    new_qty = update_stock(item, quantity, unit, action)

    reply = f"✅ {item}: now {new_qty} {unit}"

    # 🔥 ONLY ADDITION (NO CHANGE IN LOGIC)
    if new_qty == 0:
        reply += "\n🚨 Out of stock!"
    elif new_qty < 5:
        reply += "\n⚠️ Low stock! Order soon"

    return PlainTextResponse(reply)