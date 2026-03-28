from fastapi import FastAPI, Request
import os
import requests

app = FastAPI()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.get("/")
def home():
    return {"status": "running"}

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    # extract items
    items = data if isinstance(data, list) else data.get("items", [])

    for item in items:
        title = item.get("title", "No title")
        price = item.get("price", "N/A")
        url = item.get("url", "")

        message = f"🔥 New Item\n\n{title}\n€{price}\n\n{url}"

        send_telegram(message)

    return {"ok": True}

def send_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text
    })
