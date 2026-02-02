import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task
def handle_course_completion(enrollment_id):
    """
    Background task triggered when a student completes all lessons in a course.
    """
    from .models import Enrollment

    try:
        enrollment = Enrollment.objects.select_related("student", "course").get(
            id=enrollment_id
        )

        logger.info(
            f"Course completion: Student '{enrollment.student.full_name}' "
            f"completed course '{enrollment.course.title}'"
        )

        # Add any additional logic here:
        # - Send congratulation email
        # - Issue certificate
        # - Award points/badges
        # - Notify instructor

        return {
            "status": "success",
            "enrollment_id": enrollment_id,
            "student": enrollment.student.full_name,
            "course": enrollment.course.title,
        }

    except Enrollment.DoesNotExist:
        logger.error(f"Enrollment with id {enrollment_id} not found")
        return {"status": "error", "message": "Enrollment not found"}
