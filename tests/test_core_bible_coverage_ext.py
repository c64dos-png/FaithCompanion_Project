"""
Coverage Extension für src/core_bible
Strategie: Boundary verse parsing, invalid ranges, missing translations
Basiert auf echter Code-Struktur (REVIDIERT)
"""

import pytest
from src.core_bible.verse_parser import VerseParser
from src.core_bible.bible_service import BibleService
from src.core_bible.models import VerseRange


class TestVerseParseBoundaries:
    """Test edge cases in verse parsing"""
    
    def test_parse_single_verse(self):
        """Test parsing single verse reference"""
        parser = VerseParser()
        result = parser.parse_reference("John 3:16")
        assert result is not None
        assert result.book_id == "jhn"  # Normalized
        assert result.chapter == 3
        assert result.start_verse == 16
        assert result.end_verse == 16
    
    def test_parse_verse_range(self):
        """Test parsing verse range"""
        parser = VerseParser()
        result = parser.parse_reference("John 3:16-18")
        assert result is not None
        assert result.start_verse == 16
        assert result.end_verse == 18
    
    def test_parse_invalid_format(self):
        """Test parsing invalid reference format"""
        parser = VerseParser()
        result = parser.parse_reference("InvalidFormat")
        assert result is None
    
    def test_parse_invalid_book(self):
        """Test parsing unknown book name"""
        parser = VerseParser()
        result = parser.parse_reference("UnknownBook 3:16")
        assert result is None
    
    def test_is_valid_reference(self):
        """Test is_valid_reference method"""
        parser = VerseParser()
        assert parser.is_valid_reference("John 3:16") is True
        assert parser.is_valid_reference("InvalidFormat") is False


class TestBibleServiceErrors:
    """Test error handling in BibleService"""
    
    def test_get_verse_nonexistent_book(self):
        """Test requesting verse from non-existent book"""
        service = BibleService()
        result = service.get_verse("esv", "nonexistent", 1, 1)
        assert result is None
    
    def test_get_verse_nonexistent_translation(self):
        """Test requesting verse with invalid translation"""
        service = BibleService()
        result = service.get_verse("NONEXISTENT", "jhn", 3, 16)
        assert result is None
    
    def test_get_verses_with_range(self):
        """Test get_verses with VerseRange"""
        service = BibleService()
        verse_range = VerseRange(book_id="jhn", chapter=3, start_verse=16, end_verse=18)
        result = service.get_verses("esv", verse_range)
        assert isinstance(result, list)
    
    def test_get_book_metadata(self):
        """Test getting book metadata"""
        service = BibleService()
        book = service.get_book("jhn")
        assert book is not None
        assert book.name == "John"
    
    def test_get_translation_metadata(self):
        """Test getting translation metadata"""
        service = BibleService()
        translation = service.get_translation("esv")
        assert translation is not None
        assert translation.name == "English Standard Version"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
