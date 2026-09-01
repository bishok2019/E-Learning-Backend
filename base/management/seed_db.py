#!/usr/bin/env python3
"""
Database seeding script to populate tables with random data.
Generates up to 20 items per table with realistic data using Faker.

Usage:
    python seed_db.py
"""

import random
from datetime import datetime, timedelta, timezone
from typing import List

from faker import Faker
from sqlalchemy.exc import IntegrityError

from apps.api_logs.models import APILog, ErrorLog, HTTPMethod
from apps.authentication.models import (
    CustomPermission,
    CustomRole,
    CustomUser,
    PermissionCategory,
    UserType,
)
from apps.authentication.utils import hash_password
from apps.course.models import Course, CourseStatus, Lesson
from apps.database import SessionLocal
from apps.enrollment.models import Enrollment, Progress

fake = Faker()

# Configuration
NUM_ITEMS = 20  # Max items per table
SEED_VALUE = 42  # For reproducibility (optional)
HASHED_PASSWORD = hash_password(
    "password123"
)  # Default hashed password for seeded users
# Uncomment to set seed for reproducibility
# random.seed(SEED_VALUE)
# Faker.seed(SEED_VALUE)


def clear_all_tables(session):
    """Clear all tables to start fresh (optional - uncomment to use)"""
    print("Clearing existing data...")
    try:
        session.query(Progress).delete()
        session.query(Enrollment).delete()
        session.query(Lesson).delete()
        session.query(Course).delete()
        session.query(APILog).delete()
        session.query(ErrorLog).delete()
        session.query(CustomUser).delete()
        session.query(CustomPermission).delete()
        session.query(CustomRole).delete()
        session.query(PermissionCategory).delete()
        session.commit()
        print("✓ All tables cleared")
    except Exception as e:
        session.rollback()
        print(f"✗ Error clearing tables: {e}")


def seed_permission_categories(session) -> List[PermissionCategory]:
    """Seed permission categories"""
    print("\n📋 Seeding Permission Categories...")
    categories = [
        PermissionCategory(name="User Management"),
        PermissionCategory(name="Course Management"),
        PermissionCategory(name="Content Management"),
        PermissionCategory(name="Enrollment Management"),
        PermissionCategory(name="System Administration"),
    ]

    for category in categories:
        try:
            session.add(category)
        except IntegrityError:
            session.rollback()

    session.commit()
    result = session.query(PermissionCategory).all()
    print(f"✓ Created {len(result)} permission categories")
    return result


def seed_permissions(
    session, categories: List[PermissionCategory]
) -> List[CustomPermission]:
    """Seed permissions"""
    print("\n🔐 Seeding Permissions...")
    permission_templates = [
        ("Can Create User", "can_create_user"),
        ("Can Edit User", "can_edit_user"),
        ("Can Delete User", "can_delete_user"),
        ("Can View Users", "can_view_users"),
        ("Can Create Course", "can_create_course"),
        ("Can Edit Course", "can_edit_course"),
        ("Can Delete Course", "can_delete_course"),
        ("Can View Courses", "can_view_courses"),
        ("Can Create Lesson", "can_create_lesson"),
        ("Can Edit Lesson", "can_edit_lesson"),
        ("Can Delete Lesson", "can_delete_lesson"),
        ("Can Enroll Student", "can_enroll_student"),
        ("Can View Enrollments", "can_view_enrollments"),
        ("Can Create Content", "can_create_content"),
        ("Can Edit Content", "can_edit_content"),
        ("Can Delete Content", "can_delete_content"),
        ("Can Manage Permissions", "can_manage_permissions"),
        ("Can Manage Roles", "can_manage_roles"),
        ("Can View Reports", "can_view_reports"),
        # ("Can System Settings", "can_system_settings"),
    ]

    permissions = []
    for name, code_name in permission_templates:
        try:
            category = random.choice(categories)
            permission = CustomPermission(
                name=name,
                code_name=code_name,
                category_id=category.id,
            )
            session.add(permission)
            permissions.append(permission)
        except IntegrityError:
            session.rollback()

    session.commit()
    result = session.query(CustomPermission).all()
    print(f"✓ Created {len(result)} permissions")
    return result


def seed_roles(session, permissions: List[CustomPermission]) -> List[CustomRole]:
    """Seed roles"""
    print("\n👥 Seeding Roles...")
    roles_data = [
        ("Admin", "Full system access", True),
        ("Teacher", "Can manage courses and lessons", True),
        ("Student", "Can view courses and enroll", True),
        ("Moderator", "Can moderate content", True),
        ("Guest", "Read-only access", True),
    ]

    roles = []
    for name, description, is_active in roles_data:
        try:
            role = CustomRole(
                name=name,
                description=description,
                is_active=is_active,
            )
            # Assign random permissions to role
            role.permissions = random.sample(
                permissions, min(random.randint(3, 8), len(permissions))
            )
            session.add(role)
            roles.append(role)
        except IntegrityError:
            session.rollback()

    session.commit()
    result = session.query(CustomRole).all()
    print(f"✓ Created {len(result)} roles")
    return result


def seed_users(session, roles: List[CustomRole]) -> List[CustomUser]:
    """Seed users (without role assignment)"""
    print("\n👤 Seeding Users...")
    user_types = [UserType.STUDENT, UserType.TEACHER, UserType.SYSTEM]
    users = []

    for i in range(NUM_ITEMS):
        try:
            first_name = fake.first_name()
            last_name = fake.last_name()
            user = CustomUser(
                username=fake.user_name(),
                email=fake.email(),
                full_name=f"{first_name} {last_name}",
                hashed_password=HASHED_PASSWORD,
                is_active=True,
                is_superuser=i == 0,  # First user is superuser
                user_type=random.choice(user_types),
            )
            # Note: Roles are NOT assigned to users here
            session.add(user)
            users.append(user)
        except IntegrityError:
            session.rollback()

    session.commit()
    result = session.query(CustomUser).all()
    print(f"✓ Created {len(result)} users (no roles assigned)")
    return result


def seed_courses(session, teachers: List[CustomUser]) -> List[Course]:
    """Seed courses"""
    print("\n📚 Seeding Courses...")
    course_titles = [
        "Introduction to Python",
        "Web Development with FastAPI",
        "Machine Learning Basics",
        "Advanced JavaScript",
        "Database Design",
        "Cloud Computing Fundamentals",
        "Data Science with Python",
        "Mobile App Development",
        "DevOps and Docker",
        "API Design Best Practices",
        "Cybersecurity Essentials",
        "UI/UX Design Principles",
        "Blockchain Fundamentals",
        "Artificial Intelligence",
        "Big Data Analytics",
        "Software Architecture",
        "Microservices Design",
        "Testing and QA",
        "Agile Development",
        "Leadership for Developers",
    ]

    courses = []
    for i, title in enumerate(course_titles[:NUM_ITEMS]):
        try:
            instructor = random.choice(teachers)
            course = Course(
                title=title,
                description=fake.paragraph(nb_sentences=3),
                status=random.choice(
                    [CourseStatus.DRAFT, CourseStatus.PUBLISHED, CourseStatus.ARCHIVED]
                ),
                instructor_id=instructor.id,
                is_active=random.choice([True, True, True, False]),  # 75% active
            )
            session.add(course)
            courses.append(course)
        except IntegrityError:
            session.rollback()

    session.commit()
    result = session.query(Course).all()
    print(f"✓ Created {len(result)} courses")
    return result


def seed_lessons(session, courses: List[Course]) -> List[Lesson]:
    """Seed lessons"""
    print("\n📖 Seeding Lessons...")
    lesson_titles = [
        "Getting Started",
        "Fundamentals",
        "Core Concepts",
        "Advanced Topics",
        "Best Practices",
        "Real-world Examples",
        "Hands-on Projects",
        "Troubleshooting",
        "Performance Optimization",
        "Security Considerations",
        "Testing Strategies",
        "Deployment",
        "Monitoring and Logging",
        "Team Collaboration",
        "Career Path",
    ]

    lessons = []
    for course in courses:
        num_lessons = random.randint(3, 10)  # Reduced max lessons per course
        used_titles = set()
        for order in range(num_lessons):
            try:
                # Generate unique title for this course
                while True:
                    base_title = random.choice(lesson_titles)
                    lesson_title = f"{base_title} - Lesson {order + 1}"
                    if lesson_title not in used_titles:
                        used_titles.add(lesson_title)
                        break

                lesson = Lesson(
                    course_id=course.id,
                    title=lesson_title,
                    content=fake.paragraph(nb_sentences=10),
                    order=order + 1,
                )
                session.add(lesson)
                lessons.append(lesson)
            except IntegrityError:
                session.rollback()
                continue

    session.commit()
    result = session.query(Lesson).all()
    print(f"✓ Created {len(result)} lessons")
    return result


def seed_enrollments(
    session, students: List[CustomUser], courses: List[Course]
) -> List[Enrollment]:
    """Seed enrollments"""
    print("\n📝 Seeding Enrollments...")
    enrollments = []

    # Create enrollments for students
    for student in students:
        num_enrollments = random.randint(1, min(5, len(courses)))
        selected_courses = random.sample(courses, num_enrollments)

        for course in selected_courses:
            try:
                is_completed = random.choice(
                    [True, False, False, False]
                )  # 25% completed
                enrollment = Enrollment(
                    student_id=student.id,
                    course_id=course.id,
                    is_completed=is_completed,
                    completed_at=datetime.now(timezone.utc)
                    - timedelta(days=random.randint(1, 365))
                    if is_completed
                    else None,
                )
                session.add(enrollment)
                enrollments.append(enrollment)
            except IntegrityError:
                session.rollback()

    session.commit()
    result = session.query(Enrollment).all()
    print(f"✓ Created {len(result)} enrollments")
    return result


def seed_progress(
    session, enrollments: List[Enrollment], lessons: List[Lesson]
) -> List[Progress]:
    """Seed lesson completion progress"""
    print("\n✅ Seeding Progress...")
    progress_records = []

    for enrollment in enrollments:
        course_lessons = (
            session.query(Lesson).filter(Lesson.course_id == enrollment.course_id).all()
        )

        # Create progress for some lessons
        if course_lessons:
            num_completed = random.randint(0, len(course_lessons))
            completed_lessons = random.sample(course_lessons, num_completed)

            for lesson in completed_lessons:
                try:
                    progress = Progress(
                        enrollment_id=enrollment.id,
                        lesson_id=lesson.id,
                    )
                    session.add(progress)
                    progress_records.append(progress)
                except IntegrityError:
                    session.rollback()

    session.commit()
    result = session.query(Progress).all()
    print(f"✓ Created {len(result)} progress records")
    return result


def seed_api_logs(session, users: List[CustomUser]):
    """Seed API logs"""
    print("\n📊 Seeding API Logs...")
    api_endpoints = [
        "/api/v1/auth/login",
        "/api/v1/auth/register",
        "/api/v1/auth/refresh",
        "/api/v1/users",
        "/api/v1/users/{id}",
        "/api/v1/courses",
        "/api/v1/courses/{id}",
        "/api/v1/enrollments",
        "/api/v1/lessons",
    ]
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    status_codes = ["200", "201", "400", "401", "404", "500"]

    logs = []
    for i in range(NUM_ITEMS):
        try:
            log = APILog(
                url=random.choice(api_endpoints),
                method=random.choice(methods),
                ip=fake.ipv4(),
                user_agent=fake.user_agent(),
                body={"data": fake.word()} if random.choice([True, False]) else None,
                response={"status": "success"}
                if random.choice([True, False])
                else None,
                user_id=random.choice([u.id for u in users] + [None]),
                status_code=random.choice(status_codes),
            )
            session.add(log)
            logs.append(log)
        except IntegrityError:
            session.rollback()

    session.commit()
    print(f"✓ Created {len(logs)} API logs")


def seed_error_logs(session):
    """Seed error logs"""
    print("\n⚠️  Seeding Error Logs...")
    error_endpoints = [
        "/api/v1/auth/login",
        "/api/v1/users/{id}",
        "/api/v1/courses/{id}",
    ]
    methods = [HTTPMethod.get, HTTPMethod.post, HTTPMethod.put, HTTPMethod.delete]

    error_logs = []
    for i in range(NUM_ITEMS):
        try:
            error_log = ErrorLog(
                url=random.choice(error_endpoints),
                method=random.choice(methods),
                ip=fake.ipv4(),
                user_agent=fake.user_agent(),
                response={"error": fake.sentence()},
            )
            session.add(error_log)
            error_logs.append(error_log)
        except IntegrityError:
            session.rollback()

    session.commit()
    print(f"✓ Created {len(error_logs)} error logs")


def seed_db():
    """Main seeding function"""
    print("=" * 60)
    print("🌱 DATABASE SEEDING SCRIPT")
    print("=" * 60)

    session = SessionLocal()

    try:
        # Uncomment the line below to clear all tables before seeding
        # clear_all_tables(session)

        # Seed in dependency order
        categories = seed_permission_categories(session)
        permissions = seed_permissions(session, categories)
        roles = seed_roles(session, permissions)
        users = seed_users(session, roles)

        # Separate teachers and students for better data relationships
        teachers = [u for u in users if u.user_type == UserType.TEACHER] or users[:5]
        students = [u for u in users if u.user_type == UserType.STUDENT] or users[5:]

        courses = seed_courses(session, teachers)
        lessons = seed_lessons(session, courses)
        enrollments = seed_enrollments(session, students, courses)
        seed_progress(session, enrollments, lessons)
        # seed_api_logs(session, users)
        # seed_error_logs(session)

        print("\n" + "=" * 60)
        print("✨ DATABASE SEEDING COMPLETED SUCCESSFULLY!")
        print("=" * 60)

    except Exception as e:
        session.rollback()
        print(f"\n❌ Error during seeding: {e}")
        raise
    finally:
        session.close()


# if __name__ == "__main__":
#     main()
