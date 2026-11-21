from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class Outcome:
    platform: str
    status: str
    posted_url: str | None = None
    public_access: bool = False
    date: str | None = None
    time: str | None = None
    error: str | None = None

class Platform(ABC):
    name = "Unknown"

    @abstractmethod
    async def publish(self, message: str) -> Outcome:
        pass

    def ok(self, url=None, public=False):
        now = datetime.now(timezone.utc)
        return Outcome(self.name, "success", url, public, now.date().isoformat(),
                       now.time().replace(microsecond=0).isoformat(), None)

    def fail(self, error):
        return Outcome(self.name, "failed", error=str(error)[:500])
