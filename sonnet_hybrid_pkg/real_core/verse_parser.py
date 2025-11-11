"""
Verse Parser
Parse Bible verse references from text strings
"""

import re
from typing import Optional
from .models import VerseRange


class VerseParser:
    """
    Parse Bible verse references
    
    Supports formats:
    - "John 3:16"
    - "jhn 3:16"
    - "John 3:16-17"
    - "Romans 8:1-4"
    """
    
    # Book abbreviations mapping
    BOOK_ABBREVIATIONS = {
        "gen": "gen", "genesis": "gen",
        "exo": "exo", "exodus": "exo",
        "mat": "mat", "matthew": "mat",
        "jhn": "jhn", "john": "jhn",
        "rom": "rom", "romans": "rom",
    }
    
    def parse_reference(self, reference: str) -> Optional[VerseRange]:
        """
        Parse a verse reference string
        
        Args:
            reference: Reference string (e.g., "John 3:16" or "John 3:16-17")
            
        Returns:
            VerseRange or None if invalid
        """
        # Pattern: Book Chapter:Verse or Book Chapter:Verse-Verse
        pattern = r'([a-zA-Z]+)\s*(\d+):(\d+)(?:-(\d+))?'
        match = re.match(pattern, reference.strip(), re.IGNORECASE)
        
        if not match:
            return None
        
        book_name, chapter, start_verse, end_verse = match.groups()
        
        # Normalize book name
        book_id = self._normalize_book_name(book_name)
        if not book_id:
            return None
        
        # Parse numbers
        try:
            chapter_num = int(chapter)
            start_verse_num = int(start_verse)
            end_verse_num = int(end_verse) if end_verse else start_verse_num
            
            return VerseRange(
                book_id=book_id,
                chapter=chapter_num,
                start_verse=start_verse_num,
                end_verse=end_verse_num
            )
        except ValueError:
            return None
    
    def _normalize_book_name(self, book_name: str) -> Optional[str]:
        """Normalize book name to standard ID"""
        normalized = book_name.lower().strip()
        return self.BOOK_ABBREVIATIONS.get(normalized)
    
    def is_valid_reference(self, reference: str) -> bool:
        """Check if reference string is valid"""
        return self.parse_reference(reference) is not None
