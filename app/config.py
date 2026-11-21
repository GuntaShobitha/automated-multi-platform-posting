from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    mastodon_base_url: str = ""
    mastodon_access_token: str = ""
    bluesky_pds_url: str = "https://bsky.social"
    bluesky_identifier: str = ""
    bluesky_app_password: str = ""
    reddit_client_id: str = ""
    reddit_client_secret: str = ""
    reddit_username: str = ""
    reddit_password: str = ""
    reddit_user_agent: str = "automated-posting/1.0"
    reddit_subreddit: str = ""
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    discord_webhook_url: str = ""

settings = Settings()
