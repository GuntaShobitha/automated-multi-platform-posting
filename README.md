# Automated Multi-Platform Posting System

FastAPI application that validates one message (maximum 200 characters, exactly one valid HTTP(S) CTA URL) and independently attempts publishing to Mastodon, Bluesky, Reddit, Telegram and Discord.

## Stack
Python 3.10+, FastAPI, Uvicorn, Pydantic, HTTPX, pytest.

## Official API references
- Mastodon: https://docs.joinmastodon.org/methods/statuses/
- Bluesky: https://docs.bsky.app/docs/api/com-atproto-repo-create-record
- Reddit: https://www.reddit.com/dev/api/
- Telegram: https://core.telegram.org/bots/api#sendmessage
- Discord: https://discord.com/developers/docs/resources/webhook

## Setup (Windows / VS Code)
Open this folder in VS Code and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add credentials. Keep `.env` private; it is ignored by Git.

### Credentials
- Mastodon: instance URL and access token with `write:statuses` scope.
- Bluesky: handle and app password (not your main password).
- Reddit: developer app credentials, user OAuth credentials and a subreddit where the account can post. Reddit may restrict password-grant OAuth; if unavailable, use Reddit's currently approved authorization-code flow rather than bypassing restrictions.
- Telegram: create a bot using @BotFather, add it to your channel/group, then set bot token and target chat ID.
- Discord: create an incoming webhook for a channel you control and set its webhook URL.

Only configure platforms for which you have permission. Blank credentials cause that integration to return a failed result; other integrations still run.

## Run
From the project root:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 4000 --reload
```

Open http://localhost:4000/docs.

## Test request
Use Swagger `POST /posting` > Try it out:

```json
{
  "message": "Check out our latest business platform: https://example.com"
}
```

Or PowerShell:

```powershell
$body = @{ message = "Check out our latest business platform: https://example.com" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:4000/posting" -Method Post -ContentType "application/json" -Body $body
```

Run tests:

```bash
pytest -v
```

## Response behaviour
Each result includes platform, status, posted_url, public_access, date, time and error. Dates/times are UTC. `success` means at least one platform accepted the post. Inspect individual results.

Public visibility is deliberately conservative: Mastodon is marked public when the API returns a URL for a public status; Telegram is marked public only for a public channel username; Reddit and Discord are false because this MVP does not independently verify public visibility. A successful API response does not prove that every user can see a post.

## GitHub submission
Create a public repository, then run:

```bash
git init
git add .
git status
git commit -m "Build automated multi-platform posting API"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/automated-multi-platform-posting.git
git push -u origin main
```

Check that `.env` is not staged before pushing. If a secret is exposed, revoke/rotate it immediately.

## Design notes and limitations
- Integrations run concurrently with independent error handling.
- This is a request/response MVP, not a durable background job queue.
- Platform scopes, app approvals, moderation, rate limits and text constraints may reject posts.
- Reddit's password grant may not be available for every app; follow Reddit's current developer requirements.
- Add retries/idempotency, durable logs, rate limiting, authorization-code OAuth and a queue before production use.
