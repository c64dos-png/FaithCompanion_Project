"""
Bible Models
Data models for Bible text, verses, books, and translations
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class BibleTestament(str, Enum):
    """Testament enumeration"""
    OLD = "old"
    NEW = "new"


class BibleTranslation(BaseModel):
    """Bible translation model"""
    id: str
    name: str
    abbreviation: str
    language: str = "en"
    year: Optional[int] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "esv",
                "name": "English Standard Version",
                "abbreviation": "ESV",
                "language": "en",
                "year": 2001
            }
        }


class BibleBook(BaseModel):
    """Bible book model"""
    id: str
    name: str
    abbreviation: str
    testament: BibleTestament
    order: int
    chapter_count: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "gen",
                "name": "Genesis",
                "abbreviation": "Gen",
                "testament": "old",
                "order": 1,
                "chapter_count": 50
            }
        }


class BibleVerse(BaseModel):
    """Bible verse model"""
    translation_id: str
    book_id: str
    chapter: int = Field(..., ge=1)
    verse: int = Field(..., ge=1)
    text: str
    
    @property
    def reference(self) -> str:
        """Get full verse reference (e.g., 'John 3:16')"""
        return f"{self.book_id} {self.chapter}:{self.verse}"
    
    class Config:
        json_schema_extra = {
            "example": {
                "translation_id": "esv",
                "book_id": "jhn",
                "chapter": 3,
                "verse": 16,
                "text": "For God so loved the world..."
            }
        }


class VerseRange(BaseModel):
    """Verse range model for multi-verse passages"""
    book_id: str
    chapter: int
    start_verse: int
    end_verse: int
    
    def __str__(self) -> str:
        if self.start_verse == self.end_verse:
            return f"{self.book_id} {self.chapter}:{self.start_verse}"
        return f"{self.book_id} {self.chapter}:{self.start_verse}-{self.end_verse}"
