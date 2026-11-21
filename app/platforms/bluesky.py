from datetime import datetime, timezone
import httpx
from app.config import settings
from .base import Platform

class Bluesky(Platform):
    name = "Bluesky"
    async def publish(self, message):
        if not settings.bluesky_identifier or not settings.bluesky_app_password:
            return self.fail("Bluesky credentials are not configured.")
        base = settings.bluesky_pds_url.rstrip("/")
        try:
            async with httpx.AsyncClient(timeout=25) as c:
                s = await c.post(base + "/xrpc/com.atproto.server.createSession",
                    json={"identifier": settings.bluesky_identifier, "password": settings.bluesky_app_password})
                s.raise_for_status()
                session = s.json()
                p = await c.post(base + "/xrpc/com.atproto.repo.createRecord",
                    headers={"Authorization": "Bearer " + session["accessJwt"]},
                    json={"repo": session["did"], "collection": "app.bsky.feed.post",
                          "record": {"$type": "app.bsky.feed.post", "text": message,
                                     "createdAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")}})
                p.raise_for_status()
                uri = p.json().get("uri", "")
            parts = uri.split("/")
            url = f"https://bsky.app/profile/{parts[2]}/post/{parts[-1]}" if len(parts) >= 5 else None
            return self.ok(url, bool(url))
        except (httpx.HTTPError, KeyError, ValueError) as e:
            return self.fail(f"Bluesky API error: {e}")
