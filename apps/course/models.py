import enum as PyEnum  # Purpose: Define enum values

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy import Enum as SQLEnum  # Purpose: Store enum values in DB
from sqlalchemy.orm import relationship

from base.models import BaseModel


class CourseStatus(PyEnum.Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"
    UNDER_REVIEW = "UNDER_REVIEW"


class Currency(BaseModel):
    __tablename__ = "currencies"

    code = Column(String(3), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    symbol = Column(String(10), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    decimal_places = Column(Integer, default=2, nullable=False)


class Course(BaseModel):
    __tablename__ = "courses"
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(SQLEnum(CourseStatus), default=CourseStatus.DRAFT, nullable=False)
    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    requires_payment = Column(Boolean, default=False, nullable=False)
    price = Column(Numeric(10, 2), nullable=True)
    currency_id = Column(Integer, ForeignKey("currencies.id"), nullable=True)

    currency = relationship(
        "Currency",
    )

    instructor = relationship(
        "CustomUser",
        back_populates="courses",
    )
    lessons = relationship(
        "Lesson",
        back_populates="course",
        cascade="all, delete-orphan",
    )
    enrollments = relationship(
        "Enrollment",
        back_populates="course",
        cascade="all, delete-orphan",
    )

    @property
    def is_published(self):
        return self.status == CourseStatus.PUBLISHED

    @property
    def total_lessons(self):
        return len(self.lessons)


class Lesson(BaseModel):
    __tablename__ = "lessons"

    course_id = Column(
        Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False
    )
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=True)
    order = Column(Integer, default=0)

    course = relationship("Course", back_populates="lessons")
    completions = relationship(
        "Progress", back_populates="lesson", cascade="all, delete-orphan"
    )
    __table_args__ = (
        UniqueConstraint("course_id", "title", name="uq_course_lesson_title"),
    )
