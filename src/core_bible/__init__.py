"""
Core Bible Module - Bible Text Management
FaithCompanion v1.2-FULL-HARDENED

This module handles:
- Bible text storage and retrieval
- Verse parsing and formatting
- Book/chapter navigation
- Translation management
"""

from .models import BibleVerse, BibleBook, BibleTranslation
from .bible_service import BibleService
from .verse_parser import VerseParser

__all__ = [
    "BibleVerse",
    "BibleBook",
    "BibleTranslation",
    "BibleService",
    "VerseParser",
]

__version__ = "1.0.0"
