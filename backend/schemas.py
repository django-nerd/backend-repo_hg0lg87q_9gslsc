from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime


class Program(BaseModel):
    name: str = Field(..., description="Program title")
    slug: str = Field(..., description="URL-friendly identifier")
    description: str
    category: str = Field(..., description="e.g., reset, membership, download")
    price: Optional[float] = Field(None, ge=0)
    features: List[str] = []
    active: bool = True


class Post(BaseModel):
    title: str
    slug: str
    excerpt: str
    content: str
    tags: List[str] = []
    published: bool = True
    published_at: Optional[datetime] = None


class Testimonial(BaseModel):
    name: str
    role: Optional[str] = None
    quote: str
    rating: Optional[int] = Field(default=None, ge=1, le=5)


class Inquiry(BaseModel):
    name: str
    email: str
    message: str
    source: Optional[str] = None


class Stat(BaseModel):
    label: str
    value: str


# Note: Collection names are inferred from class names (lowercased)
