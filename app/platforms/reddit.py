import httpx
from app.config import settings
from .base import Platform

class Reddit(Platform):
    name = "Reddit"
    async def publish(self, message):
        cfg = [settings.reddit_client_id, settings.reddit_client_secret, settings.reddit_username,
               settings.reddit_password, settings.reddit_subreddit]
        if not all(cfg):
            return self.fail("Reddit OAuth credentials or subreddit are not configured.")
        try:
            async with httpx.AsyncClient(timeout=30) as c:
                a = await c.post("https://www.reddit.com/api/v1/access_token",
                    auth=(settings.reddit_client_id, settings.reddit_client_secret),
                    data={"grant_type": "password", "username": settings.reddit_username,
                          "password": settings.reddit_password},
                    headers={"User-Agent": settings.reddit_user_agent})
                a.raise_for_status()
                token = a.json().get("access_token")
                if not token:
                    return self.fail("Reddit did not return an access token.")
                r = await c.post("https://oauth.reddit.com/api/submit",
                    headers={"Authorization": "Bearer " + token, "User-Agent": settings.reddit_user_agent},
                    data={"api_type": "json", "kind": "self", "sr": settings.reddit_subreddit,
                          "title": "Update", "text": message, "resubmit": "true"})
                r.raise_for_status()
                payload = r.json()
            errors = payload.get("json", {}).get("errors", [])
            if errors:
                return self.fail(f"Reddit rejected the post: {errors}")
            d = payload.get("json", {}).get("data", {})
            url = d.get("url")
            if not url and d.get("id"):
                url = f"https://www.reddit.com/r/{settings.reddit_subreddit}/comments/{d['id']}/"
            return self.ok(url, False) if url else self.fail("Reddit response did not contain a post URL.")
        except (httpx.HTTPError, ValueError) as e:
            return self.fail(f"Reddit API error: {e}")
