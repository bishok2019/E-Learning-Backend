#!/usr/bin/env python3
"""
Test Concurrent Lesson Completion - Race condition testing
Tests what happens when multiple requests try to mark the same lesson complete simultaneously
"""

import threading
import time
from datetime import datetime

import requests

BASE_URL = "http://localhost:8000"


def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


print_header("TESTING CONCURRENT LESSON COMPLETION")

# Use existing test accounts
student_email = "seqtest@test.com"
instructor_email = "seqinst@test.com"

# Login
print("\n1. Logging in...")
resp = requests.post(
    f"{BASE_URL}/api/v1/auth_app/login",
    json={"email_address": student_email, "password": "Test@1234"},
)
student_token = resp.json()["access"]
print("   Student logged in ✓")

resp = requests.post(
    f"{BASE_URL}/api/v1/auth_app/login",
    json={"email_address": instructor_email, "password": "Test@1234"},
)
instructor_token = resp.json()["access"]
print("   Instructor logged in ✓")

# Create course
print("\n2. Creating course...")
resp = requests.post(
    f"{BASE_URL}/api/v1/course_app/courses/create",
    headers={"Authorization": f"Bearer {instructor_token}"},
    json={
        "title": f"Concurrent Test Course {datetime.now().timestamp()}",
        "description": "Testing concurrent completion",
    },
)
course_data = resp.json()
course_id = course_data["data"]["id"]
print(f"   Course ID: {course_id}")

# Publish course
requests.patch(
    f"{BASE_URL}/api/v1/course_app/courses/update/{course_id}",
    headers={"Authorization": f"Bearer {instructor_token}"},
    json={"status": "PUBLISHED"},
)
print("   Course published ✓")

# Create a lesson
print("\n3. Creating lesson...")
resp = requests.post(
    f"{BASE_URL}/api/v1/course_app/lessons/create",
    headers={"Authorization": f"Bearer {instructor_token}"},
    json={
        "course": course_id,
        "title": "Test Lesson",
        "content": "Content",
        "order": 1,
    },
)
lesson_data = resp.json()
lesson_id = lesson_data["data"]["id"]
print(f"   Lesson ID: {lesson_id}")

# Student enrolls
print("\n4. Student enrolling...")
resp = requests.post(
    f"{BASE_URL}/api/v1/course_app/enrollments/create",
    headers={"Authorization": f"Bearer {student_token}"},
    json={"course": course_id},
)
enrollment_data = resp.json()
print(f"   Response status: {resp.status_code}")
print(f"   Response data: {enrollment_data}")

# Handle both new enrollment and existing enrollment
if resp.status_code == 201:
    enrollment_id = enrollment_data.get("data", {}).get("id") or enrollment_data.get(
        "id"
    )
    print(f"   Enrollment ID: {enrollment_id}")
elif resp.status_code == 400 and "already enrolled" in str(enrollment_data):
    # Get existing enrollment
    resp = requests.get(
        f"{BASE_URL}/api/v1/course_app/enrollments/list",
        headers={"Authorization": f"Bearer {student_token}"},
    )
    enrollments = resp.json()
    enrollments_list = enrollments.get("data", enrollments.get("results", []))
    enrollment_id = next(
        (e["id"] for e in enrollments_list if e["course"] == course_id), None
    )
    print(f"   Using existing enrollment ID: {enrollment_id}")
else:
    print("   Unexpected response. Creating new student account...")
    # Register new student
    import random

    new_email = f"concurrent{random.randint(1000, 9999)}@test.com"
    requests.post(
        f"{BASE_URL}/api/v1/auth_app/signup",
        json={
            "email_address": new_email,
            "password": "Test@1234",
            "password2": "Test@1234",
            "first_name": "Concurrent",
            "last_name": "Test",
            "user_type": "STUDENT",
        },
    )
    resp = requests.post(
        f"{BASE_URL}/api/v1/auth_app/login",
        json={"email_address": new_email, "password": "Test@1234"},
    )
    student_token = resp.json()["access"]
    # Try enrollment again
    resp = requests.post(
        f"{BASE_URL}/api/v1/course_app/enrollments/create",
        headers={"Authorization": f"Bearer {student_token}"},
        json={"course": course_id},
    )
    enrollment_data = resp.json()
    enrollment_id = enrollment_data.get("data", {}).get("id") or enrollment_data.get(
        "id"
    )
    print(f"   Created new student and enrolled. Enrollment ID: {enrollment_id}")

# TEST: Concurrent completion attempts
print("\n5. TEST: Simulating 5 concurrent completion requests...")
print("   (All trying to mark the same lesson complete at the same time)")

results = []
errors = []


def mark_complete(thread_id):
    """Each thread tries to mark the same lesson complete"""
    try:
        resp = requests.post(
            f"{BASE_URL}/api/v1/course_app/progress/{enrollment_id}/completions/create",
            headers={"Authorization": f"Bearer {student_token}"},
            json={"lesson": lesson_id},
        )
        results.append(
            {
                "thread": thread_id,
                "status": resp.status_code,
                "response": resp.json() if resp.status_code != 500 else resp.text[:200],
            }
        )
    except Exception as e:
        errors.append({"thread": thread_id, "error": str(e)})


# Create and start threads
threads = []
for i in range(5):
    thread = threading.Thread(target=mark_complete, args=(i + 1,))
    threads.append(thread)

# Start all threads at roughly the same time
start_time = time.time()
for thread in threads:
    thread.start()

# Wait for all to complete
for thread in threads:
    thread.join()

end_time = time.time()

print(f"   All requests completed in {end_time - start_time:.3f}s\n")

# Analyze results
success_count = sum(1 for r in results if r["status"] == 201)
duplicate_count = sum(1 for r in results if r["status"] == 400)
server_error_count = sum(1 for r in results if r["status"] == 500)

print("   Results:")
print(f"   - 201 Created: {success_count}")
print(f"   - 400 Bad Request (duplicate): {duplicate_count}")
print(f"   - 500 Server Error: {server_error_count}")
print(f"   - Exceptions: {len(errors)}")

print("\n   Detailed responses:")
for r in results:
    status_emoji = "✅" if r["status"] == 201 else "⚠️" if r["status"] == 400 else "❌"
    print(f"   {status_emoji} Thread {r['thread']}: {r['status']}")
    if r["status"] == 400:
        response = r["response"]
        if "errors" in response:
            print(f"      Error: {response['errors']}")
        elif "lesson" in response:
            print(f"      Error: {response['lesson']}")

if errors:
    print("\n   Exceptions:")
    for e in errors:
        print(f"   ❌ Thread {e['thread']}: {e['error']}")

# Verify database state
print("\n6. Verifying database state...")
resp = requests.get(
    f"{BASE_URL}/api/v1/course_app/progress/{enrollment_id}/completions/list",
    headers={"Authorization": f"Bearer {student_token}"},
)
completions_data = resp.json()
completions = completions_data.get("data", completions_data.get("results", []))
print(f"   Total completions in database: {len(completions)}")

# Final assessment
print("\n7. Assessment:")
if success_count == 1 and duplicate_count == 4 and server_error_count == 0:
    print("   ✅ PERFECT: Exactly 1 success, 4 duplicates blocked gracefully")
    print("   ✅ No data corruption")
    print("   ✅ Race condition handled correctly")
elif success_count == 1 and duplicate_count + server_error_count == 4:
    print("   ⚠️  GOOD: Only 1 record created (no duplicates)")
    if server_error_count > 0:
        print(
            f"   ⚠️  BUT: {server_error_count} requests got 500 errors (should be 400)"
        )
        print("   💡 Recommendation: Catch IntegrityError and return 400")
elif success_count > 1:
    print(f"   ❌ FAIL: {success_count} records created (RACE CONDITION!)")
    print("   ❌ Data integrity violated")
    print("   💡 Critical: Need database-level locking or unique constraint")
else:
    print(
        f"   ⚠️  UNCLEAR: {success_count} created, {duplicate_count} blocked, {server_error_count} errors"
    )

print("\n" + "=" * 70)
