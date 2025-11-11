"""
Learn Service
Manage reading plans, study guides, devotionals, and progress tracking
"""

from typing import List, Optional, Dict
from datetime import date, timedelta
import secrets

from .models import (
    ReadingPlan, DailyReading, UserReadingProgress,
    StudyGuide, Devotional, ReadingPlanStatus, ReadingPlanType
)


class LearnService:
    """Service for managing learning content and progress"""
    
    def __init__(self):
        """Initialize learn service"""
        self._plans_db: Dict[str, ReadingPlan] = {}
        self._daily_readings_db: Dict[str, List[DailyReading]] = {}
        self._progress_db: Dict[str, UserReadingProgress] = {}
        self._study_guides_db: Dict[str, StudyGuide] = {}
        self._devotionals_db: Dict[str, Devotional] = {}
        self._initialize_sample_plans()
    
    def _initialize_sample_plans(self):
        """Initialize sample reading plans"""
        # Bible in One Year plan
        plan_id = "bible_one_year"
        self._plans_db[plan_id] = ReadingPlan(
            id=plan_id,
            name="Bible in One Year",
            description="Read through the entire Bible in 365 days",
            plan_type=ReadingPlanType.CHRONOLOGICAL,
            duration_days=365,
            total_readings=365
        )
        
        # New Testament in 30 Days
        plan_id_nt = "nt_30_days"
        self._plans_db[plan_id_nt] = ReadingPlan(
            id=plan_id_nt,
            name="New Testament in 30 Days",
            description="Read through the New Testament in one month",
            plan_type=ReadingPlanType.CANONICAL,
            duration_days=30,
            total_readings=30
        )
    
    def create_reading_plan(self, plan: ReadingPlan) -> ReadingPlan:
        """Create a new reading plan"""
        if plan.id is None:
            plan.id = secrets.token_urlsafe(16)
        self._plans_db[plan.id] = plan
        return plan
    
    def get_reading_plan(self, plan_id: str) -> Optional[ReadingPlan]:
        """Get reading plan by ID"""
        return self._plans_db.get(plan_id)
    
    def get_all_reading_plans(self, plan_type: Optional[ReadingPlanType] = None) -> List[ReadingPlan]:
        """Get all reading plans, optionally filtered by type"""
        plans = list(self._plans_db.values())
        if plan_type:
            plans = [p for p in plans if p.plan_type == plan_type]
        return plans
    
    def add_daily_reading(self, plan_id: str, reading: DailyReading) -> bool:
        """Add a daily reading to a plan"""
        if plan_id not in self._plans_db:
            return False
        
        if plan_id not in self._daily_readings_db:
            self._daily_readings_db[plan_id] = []
        
        self._daily_readings_db[plan_id].append(reading)
        return True
    
    def get_daily_reading(self, plan_id: str, day: int) -> Optional[DailyReading]:
        """Get daily reading for a specific day"""
        readings = self._daily_readings_db.get(plan_id, [])
        return next((r for r in readings if r.day_number == day), None)
    
    def start_reading_plan(self, user_id: str, plan_id: str) -> Optional[UserReadingProgress]:
        """Start a reading plan for a user"""
        plan = self.get_reading_plan(plan_id)
        if not plan:
            return None
        
        progress_key = f"{user_id}:{plan_id}"
        progress = UserReadingProgress(
            user_id=user_id,
            plan_id=plan_id,
            status=ReadingPlanStatus.IN_PROGRESS,
            start_date=date.today(),
            current_day=1
        )
        
        self._progress_db[progress_key] = progress
        return progress
    
    def get_user_progress(self, user_id: str, plan_id: str) -> Optional[UserReadingProgress]:
        """Get user's progress on a reading plan"""
        progress_key = f"{user_id}:{plan_id}"
        return self._progress_db.get(progress_key)
    
    def mark_day_complete(self, user_id: str, plan_id: str, day: int) -> Optional[UserReadingProgress]:
        """Mark a day as complete for a user"""
        progress = self.get_user_progress(user_id, plan_id)
        if not progress:
            return None
        
        progress.mark_day_complete(day)
        
        # Update completion percentage
        plan = self.get_reading_plan(plan_id)
        if plan:
            progress.completion_percentage = progress.calculate_progress(plan.total_readings)
        
        # Check if plan is completed
        if progress.completion_percentage >= 100.0:
            progress.status = ReadingPlanStatus.COMPLETED
        
        return progress
    
    def get_user_active_plans(self, user_id: str) -> List[UserReadingProgress]:
        """Get all active reading plans for a user"""
        return [
            progress for progress in self._progress_db.values()
            if progress.user_id == user_id and progress.status == ReadingPlanStatus.IN_PROGRESS
        ]
    
    def create_study_guide(self, guide: StudyGuide) -> StudyGuide:
        """Create a new study guide"""
        if guide.id is None:
            guide.id = secrets.token_urlsafe(16)
        self._study_guides_db[guide.id] = guide
        return guide
    
    def get_study_guide(self, guide_id: str) -> Optional[StudyGuide]:
        """Get study guide by ID"""
        return self._study_guides_db.get(guide_id)
    
    def search_study_guides(self, topic: str) -> List[StudyGuide]:
        """Search study guides by topic"""
        topic_lower = topic.lower()
        return [
            guide for guide in self._study_guides_db.values()
            if topic_lower in guide.topic.lower() or topic_lower in guide.title.lower()
        ]
    
    def create_devotional(self, devotional: Devotional) -> Devotional:
        """Create a new devotional"""
        if devotional.id is None:
            devotional.id = secrets.token_urlsafe(16)
        self._devotionals_db[devotional.id] = devotional
        return devotional
    
    def get_devotional(self, devotional_id: str) -> Optional[Devotional]:
        """Get devotional by ID"""
        return self._devotionals_db.get(devotional_id)
    
    def get_devotional_for_date(self, target_date: date) -> Optional[Devotional]:
        """Get devotional for a specific date"""
        return next(
            (d for d in self._devotionals_db.values() if d.date == target_date),
            None
        )
    
    def get_today_devotional(self) -> Optional[Devotional]:
        """Get today's devotional"""
        return self.get_devotional_for_date(date.today())
