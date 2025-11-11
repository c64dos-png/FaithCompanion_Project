"""
Tests for Core Bible Module
Test coverage for Bible service and verse parser
"""

import pytest
from src.core_bible.bible_service import BibleService
from src.core_bible.verse_parser import VerseParser
from src.core_bible.models import BibleVerse, BibleTestament, VerseRange


@pytest.fixture
def bible_service():
    """Create Bible service instance"""
    service = BibleService()
    # Add sample verses for testing
    service.add_verse(BibleVerse(
        translation_id="esv",
        book_id="jhn",
        chapter=3,
        verse=16,
        text="For God so loved the world, that he gave his only Son."
    ))
    service.add_verse(BibleVerse(
        translation_id="esv",
        book_id="jhn",
        chapter=3,
        verse=17,
        text="For God did not send his Son into the world to condemn the world."
    ))
    return service


@pytest.fixture
def verse_parser():
    """Create verse parser instance"""
    return VerseParser()


class TestBibleService:
    """Test Bible service functionality"""
    
    def test_get_verse(self, bible_service):
        """Test getting a single verse"""
        verse = bible_service.get_verse("esv", "jhn", 3, 16)
        
        assert verse is not None
        assert verse.book_id == "jhn"
        assert verse.chapter == 3
        assert verse.verse == 16
        assert "God so loved" in verse.text
    
    def test_get_verse_not_found(self, bible_service):
        """Test getting non-existent verse"""
        verse = bible_service.get_verse("esv", "jhn", 999, 999)
        assert verse is None
    
    def test_get_verses_range(self, bible_service):
        """Test getting verse range"""
        verse_range = VerseRange(
            book_id="jhn",
            chapter=3,
            start_verse=16,
            end_verse=17
        )
        verses = bible_service.get_verses("esv", verse_range)
        
        assert len(verses) == 2
        assert verses[0].verse == 16
        assert verses[1].verse == 17
    
    def test_add_verse(self, bible_service):
        """Test adding a new verse"""
        new_verse = BibleVerse(
            translation_id="esv",
            book_id="rom",
            chapter=8,
            verse=1,
            text="There is therefore now no condemnation."
        )
        bible_service.add_verse(new_verse)
        
        retrieved = bible_service.get_verse("esv", "rom", 8, 1)
        assert retrieved is not None
        assert retrieved.text == new_verse.text
    
    def test_get_book(self, bible_service):
        """Test getting book metadata"""
        book = bible_service.get_book("jhn")
        
        assert book is not None
        assert book.name == "John"
        assert book.testament == BibleTestament.NEW
    
    def test_get_all_books(self, bible_service):
        """Test getting all books"""
        books = bible_service.get_all_books()
        assert len(books) > 0
        assert all(b.order > 0 for b in books)
    
    def test_get_books_by_testament(self, bible_service):
        """Test filtering books by testament"""
        old_books = bible_service.get_all_books(BibleTestament.OLD)
        new_books = bible_service.get_all_books(BibleTestament.NEW)
        
        assert len(old_books) > 0
        assert len(new_books) > 0
        assert all(b.testament == BibleTestament.OLD for b in old_books)
        assert all(b.testament == BibleTestament.NEW for b in new_books)
    
    def test_get_translation(self, bible_service):
        """Test getting translation metadata"""
        translation = bible_service.get_translation("esv")
        
        assert translation is not None
        assert translation.name == "English Standard Version"
        assert translation.abbreviation == "ESV"
    
    def test_get_all_translations(self, bible_service):
        """Test getting all translations"""
        translations = bible_service.get_all_translations()
        assert len(translations) >= 3
        assert any(t.id == "esv" for t in translations)
    
    def test_search_verses(self, bible_service):
        """Test verse search"""
        results = bible_service.search_verses("esv", "God so loved")
        
        assert len(results) > 0
        assert any("God so loved" in v.text for v in results)


class TestVerseParser:
    """Test verse parser functionality"""
    
    def test_parse_single_verse(self, verse_parser):
        """Test parsing single verse reference"""
        result = verse_parser.parse_reference("John 3:16")
        
        assert result is not None
        assert result.book_id == "jhn"
        assert result.chapter == 3
        assert result.start_verse == 16
        assert result.end_verse == 16
    
    def test_parse_verse_range(self, verse_parser):
        """Test parsing verse range"""
        result = verse_parser.parse_reference("John 3:16-17")
        
        assert result is not None
        assert result.start_verse == 16
        assert result.end_verse == 17
    
    def test_parse_abbreviated_book(self, verse_parser):
        """Test parsing with abbreviated book name"""
        result = verse_parser.parse_reference("jhn 3:16")
        
        assert result is not None
        assert result.book_id == "jhn"
    
    def test_parse_invalid_reference(self, verse_parser):
        """Test parsing invalid reference"""
        result = verse_parser.parse_reference("invalid reference")
        assert result is None
    
    def test_is_valid_reference(self, verse_parser):
        """Test reference validation"""
        assert verse_parser.is_valid_reference("John 3:16") is True
        assert verse_parser.is_valid_reference("Genesis 1:1") is True
        assert verse_parser.is_valid_reference("invalid") is False
