import re
from urllib.parse import urlparse
from pydantic import BaseModel, Field, field_validator, ConfigDict

URL_RE = re.compile(r"https?://[^\\s<>]+", re.I)

class PostingRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    message: str = Field(..., min_length=1, max_length=200)

    @field_validator("message")
    @classmethod
    def check_exactly_one_url(cls, value):
        urls = URL_RE.findall(value)
        if len(urls) != 1:
            raise ValueError("Message must contain exactly one HTTP(S) URL.")
        url = urls[0].rstrip(".,!?;:)")
        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.hostname or "." not in parsed.hostname:
            raise ValueError("CTA URL must be a valid absolute HTTP(S) URL.")
        return value

class PlatformResult(BaseModel):
    platform: str
    status: str
    posted_url: str | None = None
    public_access: bool = False
    date: str | None = None
    time: str | None = None
    error: str | None = None

class PostingResponse(BaseModel):
    success: bool
    results: list[PlatformResult]
