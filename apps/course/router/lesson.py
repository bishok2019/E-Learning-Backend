from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from apps.database import get_db
from base.pagination import get_pagination_params
from base.route import StandardResponse
from base.utils.query_utils import generic_list_handler

from .. import schema as schemas
from ..models import Lesson

router = APIRouter()


@router.get("/list", response_model=StandardResponse)
def get_lessons(
    search: str = "",
    db: Session = Depends(get_db),
    pagination=Depends(get_pagination_params),
):
    """Get all Lessons with pagination"""

    query = db.query(Lesson)

    return generic_list_handler(
        query=query,
        schema=schemas.LessonListSchema,
        pagination=pagination,
        search=search,
        search_fields=[Lesson.title],
    )


@router.post(
    "/create", response_model=StandardResponse, status_code=status.HTTP_201_CREATED
)
def create_lesson(
    lesson: schemas.LessonCreateSchema,
    db: Session = Depends(get_db),
):
    """Create a new Lesson"""
    existing_lesson = (
        db.query(Lesson)
        .filter(Lesson.title == lesson.title, Lesson.course_id == lesson.course_id)
        .first()
    )
    if existing_lesson:
        return StandardResponse.error_response(
            message="Lesson with this title already exists in this course.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # valid_instructor = (
    #     db.query(CustomUser)
    #     .filter(
    #         CustomUser.user_type == "TEACHER",
    #         CustomUser.id == Lesson.instructor_id,
    #     )
    #     .first()
    # )
    # if not valid_instructor:
    #     return StandardResponse.error_response(
    #         message="Instructor user_type must be TEACHER",
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #     )

    db_lesson = Lesson(
        title=lesson.title,
        content=lesson.content,
        order=lesson.order,
        course_id=lesson.course_id,
    )
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)

    return StandardResponse.success_response(
        data=schemas.LessonRetrieveSchema.model_validate(db_lesson),
        message="Lesson created successfully.",
    )


@router.get("/retrieve/{lesson_id}", response_model=StandardResponse)
def retrieve_Lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        return StandardResponse.error_response(
            message="Lesson not Found.", status_code=status.HTTP_404_NOT_FOUND
        )
    return StandardResponse.success_response(
        data=schemas.LessonRetrieveSchema.model_validate(lesson),
        message="Lesson retrieved successfully.",
    )
