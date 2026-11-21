import asyncio
from app.platforms.base import Platform
from app.platforms.mastodon import Mastodon
from app.platforms.bluesky import Bluesky
from app.platforms.reddit import Reddit
from app.platforms.telegram import Telegram
from app.platforms.discord import Discord
from app.schemas import PlatformResult

def get_platforms() -> list[Platform]:
    # Destinations are selected internally, not supplied by the API caller.
    return [Mastodon(), Bluesky(), Reddit(), Telegram(), Discord()]

async def post_to_all(message: str) -> list[PlatformResult]:
    async def safe(platform):
        try:
            result = await platform.publish(message)
        except Exception as exc:
            result = platform.fail(f"Unexpected integration error: {exc}")
        return PlatformResult(**result.__dict__)
    return await asyncio.gather(*(safe(p) for p in get_platforms()))
