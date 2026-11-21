import httpx
from app.config import settings
from .base import Platform

class Telegram(Platform):
    name = "Telegram"
    async def publish(self, message):
        if not settings.telegram_bot_token or not settings.telegram_chat_id:
            return self.fail("Telegram bot token or chat ID is not configured.")
        endpoint = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"
        try:
            async with httpx.AsyncClient(timeout=20) as c:
                r = await c.post(endpoint, json={"chat_id": settings.telegram_chat_id, "text": message})
                r.raise_for_status()
                payload = r.json()
            if not payload.get("ok"):
                return self.fail(payload.get("description", "Telegram API returned an error."))
            result = payload["result"]
            username = result.get("chat", {}).get("username")
            mid = result.get("message_id")
            url = f"https://t.me/{username}/{mid}" if username and mid else None
            return self.ok(url, bool(url))
        except (httpx.HTTPError, KeyError, ValueError) as e:
            return self.fail(f"Telegram API error: {e}")
