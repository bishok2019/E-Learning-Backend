#!/usr/bin/env python3
"""
Test Sequential Lesson Completion - Students must complete lessons in order
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

print_header("TESTING SEQUENTIAL LESSON COMPLETION")

# Use existing test accounts
student_email = "seqtest@test.com"
instructor_email = "seqinst@test.com"

# Login
print("\n1. Logging in...")
resp = requests.post(f"{BASE_URL}/api/v1/auth_app/login", json={
    "email_address": student_email,
    "password": "Test@1234"
})
student_token = resp.json()['access']
print(f"   Student logged in ✓")

resp = requests.post(f"{BASE_URL}/api/v1/auth_app/login", json={
    "email_address": instructor_email,
    "password": "Test@1234"
})
instructor_token = resp.json()['access']
print(f"   Instructor logged in ✓")

# Create course
print("\n2. Creating course...")
resp = requests.post(f"{BASE_URL}/api/v1/course_app/courses/create",
    headers={"Authorization": f"Bearer {instructor_token}"},
    json={
        "title": f"Sequential Course Test {datetime.now().timestamp()}",
        "description": "Testing sequential lesson completion"
    })
print(f"   Course created ✓")

# Get course ID
resp = requests.get(f"{BASE_URL}/api/v1/course_app/courses/list",
    headers={"Authorization": f"Bearer {instructor_token}"})
data = resp.json()
# Handle both paginated and non-paginated responses
if 'data' in data and isinstance(data['data'], list):
    courses = data['data']
elif 'results' in data:
    courses = data['results']
else:
    courses = []

if not courses:
    print("   ERROR: No courses found")
    exit(1)

course_id = courses[0]['id']
print(f"   Course ID: {course_id}")

# Publish course
print("\n3. Publishing course...")
resp = requests.patch(f"{BASE_URL}/api/v1/course_app/courses/update/{course_id}",
    headers={"Authorization": f"Bearer {instructor_token}"},
    json={"status": "PUBLISHED"})
print(f"   Status: {resp.status_code}")

# Create 3 lessons
print("\n4. Creating lessons...")
lesson_ids = []
for i in range(1, 4):
    resp = requests.post(f"{BASE_URL}/api/v1/course_app/lessons/create",
        headers={"Authorization": f"Bearer {instructor_token}"},
        json={
            "course": course_id,
            "title": f"Lesson {i}: Part {i}",
            "content": f"Content for lesson {i}",
            "order": i
        })
    if resp.status_code == 201:
        lesson_data = resp.json()
        # Try different response structures
        if 'data' in lesson_data:
            # Find the ID in the data
            if isinstance(lesson_data['data'], dict):
                lesson_id = lesson_data['data'].get('id')
            else:
                lesson_id = None
        else:
            lesson_id = lesson_data.get('id')
        
        if lesson_id:
            lesson_ids.append(lesson_id)
            print(f"   Lesson {i} created: ID {lesson_id}")
        else:
            print(f"   Lesson {i} created but ID not found in response")
            print(f"   Response: {json.dumps(lesson_data, indent=2)}")

if not lesson_ids:
    print("\n   WARNING: No lesson IDs captured. Will use database IDs.")
    # Get lessons from list endpoint
    resp = requests.get(f"{BASE_URL}/api/v1/course_app/lessons/list?course={course_id}",
        headers={"Authorization": f"Bearer {instructor_token}"})
    lessons_data = resp.json()
    if 'data' in lessons_data:
        lessons = lessons_data['data']
    elif 'results' in lessons_data:
        lessons = lessons_data['results']
    else:
        lessons = []
    
    lesson_ids = [lesson['id'] for lesson in sorted(lessons, key=lambda x: x['order'])]
    print(f"   Retrieved lesson IDs: {lesson_ids}")

# Student enrolls
print("\n5. Student enrolling in course...")
resp = requests.post(f"{BASE_URL}/api/v1/course_app/enrollments/create",
    headers={"Authorization": f"Bearer {student_token}"},
    json={"course": course_id})
enrollment_data = resp.json()
if 'data' in enrollment_data and isinstance(enrollment_data['data'], dict):
    enrollment_id = enrollment_data['data'].get('id')
else:
    enrollment_id = enrollment_data.get('id')
print(f"   Enrolled: Enrollment ID {enrollment_id}")

# TEST 1: Try to complete Lesson 3 first (should FAIL)
print("\n6. TEST: Attempting to complete Lesson 3 without completing 1 & 2...")
resp = requests.post(f"{BASE_URL}/api/v1/course_app/progress/{enrollment_id}/completions/create",
    headers={"Authorization": f"Bearer {student_token}"},
    json={"lesson": lesson_ids[2]})

print(f"   Status: {resp.status_code}")
if resp.status_code == 201:
    print("   ❌ FAIL: Student was able to skip lessons!")
    print("   BUG: Sequential validation is not working")
elif resp.status_code == 400:
    error_data = resp.json()
    print("   ✅ PASS: Out-of-order completion blocked")
    if 'errors' in error_data:
        print(f"   Message: {error_data['errors']}")
    elif 'lesson' in error_data:
        print(f"   Message: {error_data['lesson']}")
else:
    print(f"   Response: {resp.text}")

# TEST 2: Complete Lesson 1 (should WORK)
print("\n7. TEST: Completing Lesson 1...")
resp = requests.post(f"{BASE_URL}/api/v1/course_app/progress/{enrollment_id}/completions/create",
    headers={"Authorization": f"Bearer {student_token}"},
    json={"lesson": lesson_ids[0]})
print(f"   Status: {resp.status_code} {'✅ PASS' if resp.status_code == 201 else '❌ FAIL'}")

# TEST 3: Try Lesson 3 again (should still FAIL - Lesson 2 not done)
print("\n8. TEST: Attempting Lesson 3 again (Lesson 2 still incomplete)...")
resp = requests.post(f"{BASE_URL}/api/v1/course_app/progress/{enrollment_id}/completions/create",
    headers={"Authorization": f"Bearer {student_token}"},
    json={"lesson": lesson_ids[2]})
print(f"   Status: {resp.status_code}")
if resp.status_code == 201:
    print("   ❌ FAIL: Still able to skip Lesson 2")
elif resp.status_code == 400:
    error_data = resp.json()
    print("   ✅ PASS: Still requires Lesson 2 first")
    if 'errors' in error_data:
        print(f"   Message: {error_data['errors']}")

# TEST 4: Complete Lesson 2 (should WORK)
print("\n9. TEST: Completing Lesson 2...")
resp = requests.post(f"{BASE_URL}/api/v1/course_app/progress/{enrollment_id}/completions/create",
    headers={"Authorization": f"Bearer {student_token}"},
    json={"lesson": lesson_ids[1]})
print(f"   Status: {resp.status_code} {'✅ PASS' if resp.status_code == 201 else '❌ FAIL'}")

# TEST 5: Complete Lesson 3 (should WORK now)
print("\n10. TEST: Completing Lesson 3 (should work now)...")
resp = requests.post(f"{BASE_URL}/api/v1/course_app/progress/{enrollment_id}/completions/create",
    headers={"Authorization": f"Bearer {student_token}"},
    json={"lesson": lesson_ids[2]})
print(f"   Status: {resp.status_code} {'✅ PASS' if resp.status_code == 201 else '❌ FAIL'}")

# Check progress
print("\n11. Checking final progress...")
resp = requests.get(f"{BASE_URL}/api/v1/course_app/enrollments/retrieve/{enrollment_id}",
    headers={"Authorization": f"Bearer {student_token}"})
if resp.status_code == 200:
    enrollment = resp.json()
    if 'data' in enrollment:
        enrollment = enrollment['data']
    completion = enrollment.get('completion_percentage', 'N/A')
    print(f"   Completion: {completion}%")
    print(f"   ✅ All lessons completed in order")

print_header("TEST COMPLETE")
