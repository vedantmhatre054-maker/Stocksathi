from mongo import inventory_collection, transactions_collection
from datetime import datetime


def update_stock(item, quantity, unit, action):
    product = inventory_collection.find_one({"productName": item})

    if product:
        current_qty = product["quantity"]

        if action == "add":
            new_qty = current_qty + quantity
        else:
            new_qty = current_qty - quantity

        inventory_collection.update_one(
            {"productName": item},
            {
                "$set": {
                    "quantity": new_qty,
                    "lastUpdated": datetime.now()
                }
            }
        )
    else:
        new_qty = quantity
        inventory_collection.insert_one({
            "productName": item,
            "quantity": new_qty,
            "threshold": 5,
            "lastUpdated": datetime.now()
        })

    # 🔥 Save transaction
    transactions_collection.insert_one({
        "type": "in" if action == "add" else "out",
        "quantity": quantity,
        "product": item,
        "timestamp": datetime.now()
    })

    return new_qty


def get_stock(item):
    product = inventory_collection.find_one({"productName": item})

    if product:
        return product["quantity"], "kg"
    else:
        return None, None