from mongo import users_collection

users_collection.insert_one({
    "name": "Sushant",
    "phone": "1234567890"
})

print("Mongo Connected ✅")