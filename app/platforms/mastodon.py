import httpx
from app.config import settings
from .base import Platform

class Mastodon(Platform):
    name = "Mastodon"
    async def publish(self, message):
        if not settings.mastodon_base_url or not settings.mastodon_access_token:
            return self.fail("Mastodon credentials are not configured.")
        try:
            async with httpx.AsyncClient(timeout=20) as c:
                r = await c.post(settings.mastodon_base_url.rstrip("/") + "/api/v1/statuses",
                    headers={"Authorization": "Bearer " + settings.mastodon_access_token},
                    data={"status": message, "visibility": "public"})
                r.raise_for_status()
                data = r.json()
            url = data.get("url") or data.get("uri")
            return self.ok(url, bool(url))
        except (httpx.HTTPError, ValueError) as e:
            return self.fail(f"Mastodon API error: {e}")
