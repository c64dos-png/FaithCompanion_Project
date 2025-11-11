"""
Coverage Extension für src/learn/learn_service
Strategie: Error paths, reading plans, progress tracking
Basiert auf echter Code-Struktur (REVIDIERT v2)
"""

import pytest
from src.learn.learn_service import LearnService
from src.learn.models import ReadingPlan, ReadingPlanType


class TestLearnServiceReadingPlans:
    """Test reading plan operations"""
    
    def test_create_reading_plan(self):
        """Test creating a reading plan"""
        service = LearnService()
        plan = ReadingPlan(
            id="test_plan",
            name="Test Plan",
            description="Test description",
            plan_type=ReadingPlanType.CHRONOLOGICAL,
            duration_days=30,
            total_readings=30
        )
        created = service.create_reading_plan(plan)
        assert created is not None
        assert created.id == "test_plan"
    
    def test_get_reading_plan(self):
        """Test getting existing plan"""
        service = LearnService()
        # Sample plans initialized in __init__
        plan = service.get_reading_plan("bible_one_year")
        assert plan is not None
        assert plan.name == "Bible in One Year"
    
    def test_get_nonexistent_plan(self):
        """Test getting non-existent plan"""
        service = LearnService()
        result = service.get_reading_plan("nonexistent_plan")
        assert result is None
    
    def test_get_all_reading_plans(self):
        """Test getting all plans"""
        service = LearnService()
        plans = service.get_all_reading_plans()
        assert isinstance(plans, list)
        assert len(plans) >= 2  # At least sample plans
    
    def test_get_plans_filtered_by_type(self):
        """Test filtering plans by type"""
        service = LearnService()
        plans = service.get_all_reading_plans(plan_type=ReadingPlanType.CHRONOLOGICAL)
        assert isinstance(plans, list)


class TestLearnServiceUserProgress:
    """Test user progress tracking"""
    
    def test_start_reading_plan(self):
        """Test starting a reading plan"""
        service = LearnService()
        progress = service.start_reading_plan("user_123", "bible_one_year")
        assert progress is not None
        assert progress.user_id == "user_123"
        assert progress.plan_id == "bible_one_year"
        assert progress.current_day == 1
    
    def test_start_nonexistent_plan(self):
        """Test starting non-existent plan"""
        service = LearnService()
        progress = service.start_reading_plan("user_123", "nonexistent")
        assert progress is None
    
    def test_get_user_progress(self):
        """Test getting user progress"""
        service = LearnService()
        service.start_reading_plan("user_123", "bible_one_year")
        progress = service.get_user_progress("user_123", "bible_one_year")
        assert progress is not None
    
    def test_mark_day_complete(self):
        """Test marking a day as complete"""
        service = LearnService()
        service.start_reading_plan("user_123", "bible_one_year")
        progress = service.mark_day_complete("user_123", "bible_one_year", 1)
        assert progress is not None
    
    def test_get_user_active_plans(self):
        """Test getting all active plans for user"""
        service = LearnService()
        service.start_reading_plan("user_123", "bible_one_year")
        active = service.get_user_active_plans("user_123")
        assert isinstance(active, list)
        assert len(active) > 0


class TestLearnServiceStudyGuides:
    """Test study guide operations"""
    
    def test_get_study_guide(self):
        """Test getting study guide"""
        service = LearnService()
        result = service.get_study_guide("nonexistent")
        assert result is None
    
    def test_search_study_guides(self):
        """Test searching study guides"""
        service = LearnService()
        results = service.search_study_guides("prayer")
        assert isinstance(results, list)


class TestLearnServiceDevotionals:
    """Test devotional operations"""
    
    def test_get_today_devotional(self):
        """Test getting today's devotional"""
        service = LearnService()
        result = service.get_today_devotional()
        # May be None if no devotional for today
        assert result is None or hasattr(result, 'date')
    
    def test_get_devotional(self):
        """Test getting devotional by ID"""
        service = LearnService()
        result = service.get_devotional("nonexistent")
        assert result is None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
