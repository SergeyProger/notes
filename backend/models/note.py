from beanie import Document
from pymongo import TEXT
from .base import TimestampMixin

class Note(Document, TimestampMixin):
    text: str
    title: str = "Title"

    class Settings:
        name = "texts"
        indexes = [
                    [("text", TEXT)]
                  ]