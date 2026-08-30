from datetime import datetime

from pydantic import BaseModel, ConfigDict

from apps.authentication.schema import UserRetrieve
from apps.course.schema import CourseListSchema


class EnrollmentBaseSchema(BaseModel):
    is_completed: bool
    completed_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class EnrollmentCreateSchema(EnrollmentBaseSchema):
    student_id: int
    course_id: int


class EnrollmentRetriveSchema(EnrollmentBaseSchema):
    id: int
    student: UserRetrieve
    course: CourseListSchema
