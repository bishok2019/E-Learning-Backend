from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from apps.authentication.models import CustomUser
from apps.authentication.utils import get_current_active_user
from apps.course.models import Course
from apps.course.schema.course import CourseListSchema
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
    enrollment: EnrollmentCreateSchema, db: Session = Depends(get_db)
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


@router.get("/list", response_model=StandardResponse)
def get_enrollement(
    student_id: int | None = None,
    course_id: int | None = None,
    is_completed: bool | None = None,
    db: Session = Depends(get_db),
    pagination=Depends(get_pagination_params),
):
    """Get enrollments with supported filters."""
    result = generic_list_handler(
        filter_fields=["student_id", "course_id", "is_completed"],
        model=Enrollment,
        schema=EnrollmentRetriveSchema,
        pagination=pagination,
        student_id=student_id,
        course_id=course_id,
        is_completed=is_completed,
        db=db,
    )
    return StandardResponse.success_response(
        data=result.data,
        message="Enrollment fetched successfully.",
        meta=result.meta,
    )


# @router.get("/enrolled/list", response_model=StandardResponse)
# def get_enrolled_courses(
#     db: Session = Depends(get_db),
#     current_user: CustomUser = Depends(get_current_active_user),
# ):
#     """Get all courses the current student is enrolled in."""

#     enrollments = (
#         db.query(Enrollment).filter(Enrollment.student_id == current_user.id).all()
#     )

#     courses = [enrollment.course for enrollment in enrollments]
#     print(f"Enrolled courses for student {current_user.id}: {courses}")
#     result = [CourseListSchema.model_validate(course) for course in courses]

#     print(f"Serialized enrolled courses for student {current_user.id}: {result}")

#     return StandardResponse.success_response(
#         data=result,
#         message="Enrolled courses fetched successfully.",
#         status_code=status.HTTP_200_OK,
#     )


@router.get("/enrolled/list", response_model=StandardResponse)
def get_enrolled_courses(
    db: Session = Depends(get_db),
    current_user: CustomUser = Depends(get_current_active_user),
):
    """Get all courses the current student is enrolled in."""
    # Use the generic list handler to fetch enrollments filtered by the
    # current user's id and eager-load the related course objects. This
    # provides pagination, search and filtering consistency with other
    # list endpoints.
    pagination = get_pagination_params()

    enrollments_response = generic_list_handler(
        model=Enrollment,
        schema=EnrollmentRetriveSchema,
        filter_fields=["student_id"],
        pagination=pagination,
        student_id=current_user.id,
        db=db,
        eager_loads=[Enrollment.course],
    )

    # Extract the course payloads from the enrollment serialisation
    enrollments_data = getattr(enrollments_response, "data", []) or []
    courses = [item.get("course") for item in enrollments_data]

    return StandardResponse.success_response(
        data=courses,
        message="Enrolled courses fetched successfully.",
        status_code=status.HTTP_200_OK,
        meta=getattr(enrollments_response, "meta", None),
    )
