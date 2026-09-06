from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from apps.authentication.models import CustomUser
from apps.authentication.utils import get_current_active_user
from apps.course.models import Course, Lesson
from apps.course.schema import CourseListSchema, LessonListSchema
from apps.database import get_db
from base.pagination import get_pagination_params
from base.route import StandardResponse
from base.utils.query_utils import generic_list_handler

from .models import Enrollment
from .schemas import EnrollmentCreateSchema, EnrollmentRetriveSchema

router = APIRouter()


@router.post(
    "/create", response_model=StandardResponse, status_code=status.HTTP_201_CREATED
)
def create_enrollment(
    enrollment: EnrollmentCreateSchema,
    db: Session = Depends(get_db),
    _: CustomUser = Depends(get_current_active_user),
):
    """Enroll a student in a course."""
    student = (
        db.query(CustomUser).filter(CustomUser.id == enrollment.student_id).first()
    )
    course = db.query(Course).filter(Course.id == enrollment.course_id).first()

    if not student:
        return StandardResponse.error_response(
            message="Invalid Student ID",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if not course:
        return StandardResponse.error_response(
            message="Invalid Course ID",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    existing_enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.student_id == enrollment.student_id,
            Enrollment.course_id == enrollment.course_id,
        )
        .first()
    )
    if existing_enrollment:
        return StandardResponse.error_response(
            message="Student is already enrolled in this course.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    add_enrollment = Enrollment(
        student_id=enrollment.student_id,
        course_id=enrollment.course_id,
        is_completed=enrollment.is_completed,
        completed_at=enrollment.completed_at,
    )
    db.add(add_enrollment)
    db.commit()
    db.refresh(add_enrollment)

    return StandardResponse.success_response(
        data=EnrollmentCreateSchema.model_validate(add_enrollment),
        message="Enrollment created successfully.",
        status_code=status.HTTP_201_CREATED,
    )


@router.get("/list")
def get_enrollement(
    student_id: int | None = None,
    course_id: int | None = None,
    is_completed: bool | None = None,
    db: Session = Depends(get_db),
    pagination=Depends(get_pagination_params),
):
    """Get enrollments with supported filters."""

    query = db.query(Enrollment)

    return generic_list_handler(
        query=query,
        schema=EnrollmentRetriveSchema,
        pagination=pagination,
        filters={
            Enrollment.student_id: student_id,
            Enrollment.course_id: course_id,
            Enrollment.is_completed: is_completed,
        },
        message="Enrollment fetched successfully.",
    )


@router.get("/enrolled/course/list", response_model=StandardResponse)
def get_enrolled_courses(
    db: Session = Depends(get_db),
    current_user: CustomUser = Depends(get_current_active_user),
    pagination=Depends(get_pagination_params),
    search: Optional[str] = None,
):
    """Get all courses the current student is enrolled in."""

    # Prepare the query first — join baked in, filtered to this student
    query = (
        db.query(Course)
        .join(Enrollment, Enrollment.course_id == Course.id)
        .filter(Enrollment.student_id == current_user.id)
    )

    return generic_list_handler(
        query=query,
        schema=CourseListSchema,
        pagination=pagination,
        search=search,
        search_fields=[Course.title, Course.description],
        message="Enrolled courses fetched successfully.",
    )


@router.get("/enrolled/lesson/{course_id}")
def get_enrolled_lesson(
    course_id: int,
    order: int | None = None,
    db: Session = Depends(get_db),
    current_user: CustomUser = Depends(get_current_active_user),
    pagination=Depends(get_pagination_params),
    search: Optional[str] = None,
):
    """Get all lessons for a specific course the current student is enrolled in."""

    enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.course_id == course_id,
            Enrollment.student_id == current_user.id,
        )
        .first()
    )
    if not enrollment:
        return StandardResponse.error_response(
            message="You are not enrolled in this course.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    query = db.query(Lesson).filter(Lesson.course_id == course_id)
    return generic_list_handler(
        query=query,
        schema=LessonListSchema,
        pagination=pagination,
        search=search,
        search_fields=[Lesson.title, Lesson.order],
        message="Enrolled courses fetched successfully.",
        filters={
            Lesson.course_id: course_id,
            Lesson.order: order,
        },
    )
