"""
Learn Module Models
Reading plans, study guides, devotionals, progress tracking
"""

from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class ReadingPlanType(str, Enum):
    """Reading plan type enumeration"""
    CHRONOLOGICAL = "chronological"
    CANONICAL = "canonical"
    TOPICAL = "topical"
    DEVOTIONAL = "devotional"
    CUSTOM = "custom"


class ReadingPlanStatus(str, Enum):
    """Reading plan status"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    PAUSED = "paused"


class ReadingPlan(BaseModel):
    """Reading plan model"""
    id: Optional[str] = None
    name: str
    description: str
    plan_type: ReadingPlanType
    duration_days: int = Field(..., gt=0)
    total_readings: int = Field(..., gt=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Bible in One Year",
                "description": "Read through the entire Bible in 365 days",
                "plan_type": "chronological",
                "duration_days": 365,
                "total_readings": 365
            }
        }


class DailyReading(BaseModel):
    """Daily reading assignment"""
    day_number: int = Field(..., ge=1)
    readings: List[str]  # Verse references like ["Genesis 1-3", "Psalm 1"]
    notes: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "day_number": 1,
                "readings": ["Genesis 1-3", "Psalm 1"],
                "notes": "Creation story and introduction to Psalms"
            }
        }


class UserReadingProgress(BaseModel):
    """User's progress on a reading plan"""
    user_id: str
    plan_id: str
    status: ReadingPlanStatus = ReadingPlanStatus.NOT_STARTED
    start_date: Optional[date] = None
    current_day: int = 0
    completed_days: List[int] = Field(default_factory=list)
    last_read_date: Optional[date] = None
    completion_percentage: float = Field(default=0.0, ge=0.0, le=100.0)
    
    def mark_day_complete(self, day: int):
        """Mark a day as completed"""
        if day not in self.completed_days:
            self.completed_days.append(day)
            self.completed_days.sort()
        self.last_read_date = date.today()
        
    def calculate_progress(self, total_days: int) -> float:
        """Calculate completion percentage"""
        if total_days == 0:
            return 0.0
        return (len(self.completed_days) / total_days) * 100.0


class StudyGuide(BaseModel):
    """Study guide for topics or books"""
    id: Optional[str] = None
    title: str
    topic: str
    content: str
    scripture_references: List[str]
    discussion_questions: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Understanding Grace",
                "topic": "grace",
                "content": "Grace is God's unmerited favor...",
                "scripture_references": ["Ephesians 2:8-9", "Romans 3:23-24"],
                "discussion_questions": ["What does grace mean to you?"]
            }
        }


class Devotional(BaseModel):
    """Daily devotional content"""
    id: Optional[str] = None
    title: str
    date: date
    scripture: str  # Verse reference
    content: str
    prayer: Optional[str] = None
    author: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Walking in Faith",
                "date": "2025-11-05",
                "scripture": "Hebrews 11:1",
                "content": "Faith is the assurance of things hoped for...",
                "prayer": "Lord, increase my faith..."
            }
        }
