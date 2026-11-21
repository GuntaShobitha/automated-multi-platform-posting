import httpx
from app.config import settings
from .base import Platform

class Discord(Platform):
    name = "Discord"
    async def publish(self, message):
        hook = settings.discord_webhook_url
        if not hook:
            return self.fail("Discord webhook URL is not configured.")
        endpoint = hook + ("&" if "?" in hook else "?") + "wait=true"
        try:
            async with httpx.AsyncClient(timeout=20) as c:
                r = await c.post(endpoint, json={"content": message})
                r.raise_for_status()
                r.json()  # Discord confirms creation; webhook response is not a public permalink.
            return self.ok(None, False)
        except (httpx.HTTPError, ValueError) as e:
            return self.fail(f"Discord API error: {e}")
