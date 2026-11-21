from fastapi import FastAPI
from app.schemas import PostingRequest, PostingResponse
from app.services.posting_service import post_to_all

app = FastAPI(title="Automated Multi-Platform Posting API", version="1.0.0",
              description="Validates a message and publishes it independently to configured platforms.")

@app.get("/", tags=["Health"])
async def health():
    return {"status": "online", "service": "Automated Multi-Platform Posting API"}

@app.post("/posting", response_model=PostingResponse, tags=["Publishing"])
async def posting(request: PostingRequest):
    results = await post_to_all(request.message)
    return PostingResponse(success=any(r.status == "success" for r in results), results=results)
