"""
Tests for Learn Module
Test coverage for reading plans, study guides, and devotionals
"""

import pytest
from datetime import date, datetime
from src.learn.learn_service import LearnService
from src.learn.models import (
    ReadingPlan, DailyReading, ReadingPlanType,
    ReadingPlanStatus, StudyGuide, Devotional
)


@pytest.fixture
def learn_service():
    """Create learn service instance"""
    return LearnService()


class TestReadingPlans:
    """Test reading plan management"""
    
    def test_create_reading_plan(self, learn_service):
        """Test creating a reading plan"""
        plan = ReadingPlan(
            name="Test Plan",
            description="Test description",
            plan_type=ReadingPlanType.TOPICAL,
            duration_days=7,
            total_readings=7
        )
        created = learn_service.create_reading_plan(plan)
        
        assert created.id is not None
        assert created.name == "Test Plan"
    
    def test_get_reading_plan(self, learn_service):
        """Test getting a reading plan"""
        plan = learn_service.get_reading_plan("bible_one_year")
        
        assert plan is not None
        assert plan.name == "Bible in One Year"
        assert plan.duration_days == 365
    
    def test_get_all_plans(self, learn_service):
        """Test getting all reading plans"""
        plans = learn_service.get_all_reading_plans()
        assert len(plans) >= 2
    
    def test_filter_plans_by_type(self, learn_service):
        """Test filtering plans by type"""
        chronological = learn_service.get_all_reading_plans(ReadingPlanType.CHRONOLOGICAL)
        assert all(p.plan_type == ReadingPlanType.CHRONOLOGICAL for p in chronological)


class TestDailyReadings:
    """Test daily reading management"""
    
    def test_add_daily_reading(self, learn_service):
        """Test adding a daily reading"""
        reading = DailyReading(
            day_number=1,
            readings=["Genesis 1-3"],
            notes="Creation"
        )
        result = learn_service.add_daily_reading("bible_one_year", reading)
        assert result is True
    
    def test_get_daily_reading(self, learn_service):
        """Test getting a daily reading"""
        reading = DailyReading(day_number=1, readings=["Genesis 1"])
        learn_service.add_daily_reading("bible_one_year", reading)
        
        retrieved = learn_service.get_daily_reading("bible_one_year", 1)
        assert retrieved is not None
        assert retrieved.day_number == 1


class TestUserProgress:
    """Test user progress tracking"""
    
    def test_start_reading_plan(self, learn_service):
        """Test starting a reading plan"""
        progress = learn_service.start_reading_plan("user_123", "bible_one_year")
        
        assert progress is not None
        assert progress.status == ReadingPlanStatus.IN_PROGRESS
        assert progress.start_date == date.today()
    
    def test_mark_day_complete(self, learn_service):
        """Test marking a day complete"""
        learn_service.start_reading_plan("user_123", "bible_one_year")
        progress = learn_service.mark_day_complete("user_123", "bible_one_year", 1)
        
        assert 1 in progress.completed_days
        assert progress.completion_percentage > 0
    
    def test_plan_completion(self, learn_service):
        """Test plan completion tracking"""
        # Create small plan
        plan = ReadingPlan(
            id="test_plan",
            name="Test",
            description="Test",
            plan_type=ReadingPlanType.CUSTOM,
            duration_days=2,
            total_readings=2
        )
        learn_service.create_reading_plan(plan)
        learn_service.start_reading_plan("user_123", "test_plan")
        
        # Complete all days
        learn_service.mark_day_complete("user_123", "test_plan", 1)
        progress = learn_service.mark_day_complete("user_123", "test_plan", 2)
        
        assert progress.completion_percentage == 100.0
        assert progress.status == ReadingPlanStatus.COMPLETED


class TestStudyGuides:
    """Test study guide management"""
    
    def test_create_study_guide(self, learn_service):
        """Test creating a study guide"""
        guide = StudyGuide(
            title="Test Guide",
            topic="faith",
            content="Content here",
            scripture_references=["Hebrews 11:1"]
        )
        created = learn_service.create_study_guide(guide)
        
        assert created.id is not None
        assert created.title == "Test Guide"
    
    def test_search_study_guides(self, learn_service):
        """Test searching study guides"""
        guide = StudyGuide(
            title="Grace Study",
            topic="grace",
            content="About grace",
            scripture_references=["Ephesians 2:8"]
        )
        learn_service.create_study_guide(guide)
        
        results = learn_service.search_study_guides("grace")
        assert len(results) > 0
        assert any(g.topic == "grace" for g in results)


class TestDevotionals:
    """Test devotional management"""
    
    def test_create_devotional(self, learn_service):
        """Test creating a devotional"""
        devotional = Devotional(
            title="Daily Hope",
            date=date.today(),
            scripture="Psalm 23:1",
            content="The Lord is my shepherd"
        )
        created = learn_service.create_devotional(devotional)
        
        assert created.id is not None
        assert created.title == "Daily Hope"
    
    def test_get_today_devotional(self, learn_service):
        """Test getting today's devotional"""
        devotional = Devotional(
            title="Today",
            date=date.today(),
            scripture="Psalm 1:1",
            content="Blessed is the one"
        )
        learn_service.create_devotional(devotional)
        
        today = learn_service.get_today_devotional()
        assert today is not None
        assert today.date == date.today()
