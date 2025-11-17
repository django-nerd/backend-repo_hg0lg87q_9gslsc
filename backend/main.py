from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from database import db, create_document, get_documents
from schemas import Program, Post, Testimonial, Inquiry, Stat

app = FastAPI(title="Unshakeable Discipline API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "service": "unshakeable-discipline"}


@app.get("/test")
async def test_db():
    # Verify database connection via a simple list call
    try:
        await db.list_collection_names()
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Programs
@app.post("/programs", response_model=dict)
async def create_program(program: Program):
    doc = await create_document("program", program.dict())
    return {"inserted_id": str(doc.inserted_id)}


@app.get("/programs", response_model=List[Program])
async def list_programs(category: Optional[str] = None, active: Optional[bool] = None):
    filt = {}
    if category is not None:
        filt["category"] = category
    if active is not None:
        filt["active"] = active
    docs = await get_documents("program", filt, limit=100)
    return [Program(**d) for d in docs]


# Posts
@app.post("/posts", response_model=dict)
async def create_post(post: Post):
    data = post.dict()
    if data.get("published") and not data.get("published_at"):
        data["published_at"] = datetime.utcnow()
    doc = await create_document("post", data)
    return {"inserted_id": str(doc.inserted_id)}


@app.get("/posts", response_model=List[Post])
async def list_posts(tag: Optional[str] = None, published: bool = True):
    filt = {"published": published}
    if tag:
        filt["tags"] = {"$in": [tag]}
    docs = await get_documents("post", filt, limit=100)
    return [Post(**d) for d in docs]


# Testimonials & stats (for social proof)
@app.post("/testimonials", response_model=dict)
async def create_testimonial(t: Testimonial):
    doc = await create_document("testimonial", t.dict())
    return {"inserted_id": str(doc.inserted_id)}


@app.get("/testimonials", response_model=List[Testimonial])
async def list_testimonials():
    docs = await get_documents("testimonial", {}, limit=50)
    return [Testimonial(**d) for d in docs]


@app.post("/stats", response_model=dict)
async def create_stat(s: Stat):
    doc = await create_document("stat", s.dict())
    return {"inserted_id": str(doc.inserted_id)}


@app.get("/stats", response_model=List[Stat])
async def list_stats():
    docs = await get_documents("stat", {}, limit=50)
    return [Stat(**d) for d in docs]


# Contact / coaching inquiries
@app.post("/inquiries", response_model=dict)
async def create_inquiry(i: Inquiry):
    doc = await create_document("inquiry", i.dict())
    return {"inserted_id": str(doc.inserted_id)}
