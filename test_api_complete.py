#!/usr/bin/env python3
"""
Comprehensive API Test Script for E-Learning Backend
Run: python3 test_api_complete.py
"""

import json
from datetime import datetime

import requests

BASE_URL = "http://localhost:8000"


def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)


def print_test(num, name):
    print(f"\n✓ Test {num}: {name}")


def print_result(status_code, expected_codes, details=""):
    if isinstance(expected_codes, int):
        expected_codes = [expected_codes]

    passed = status_code in expected_codes
    status_text = f"{'✅ PASS' if passed else '❌ FAIL'}"
    print(f"   Status: {status_code} {status_text}")
    if details:
        print(f"   {details}")
    return passed


def test_api():
    print_header("E-LEARNING BACKEND API COMPREHENSIVE TEST")
    print(f"Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    results = {"passed": 0, "failed": 0}

    # Test 1: Student Signup
    print_test(1, "Student Signup")
    resp = requests.post(
        f"{BASE_URL}/api/v1/auth_app/signup",
        json={
            "email_address": f"student_{datetime.now().timestamp()}@test.com",
            "password": "Test@1234",
            "password2": "Test@1234",
            "first_name": "John",
            "last_name": "Student",
            "user_type": "STUDENT",
        },
    )
    if print_result(resp.status_code, 201):
        data = resp.json()
        if "data" in data:
            print(f"   User Type: {data['data'].get('user_type', 'N/A')}")
            print(f"   Email: {data['data'].get('email_address', 'N/A')}")
        results["passed"] += 1
    else:
        results["failed"] += 1
        print(f"   Response: {resp.text[:200]}")

    # Test 2: Instructor Signup
    print_test(2, "Instructor Signup")
    instructor_email = f"instructor_{datetime.now().timestamp()}@test.com"
    resp = requests.post(
        f"{BASE_URL}/api/v1/auth_app/signup",
        json={
            "email_address": instructor_email,
            "password": "Test@1234",
            "password2": "Test@1234",
            "first_name": "Jane",
            "last_name": "Instructor",
            "user_type": "INSTRUCTOR",
        },
    )
    if print_result(resp.status_code, 201):
        data = resp.json()
        if "data" in data:
            print(f"   User Type: {data['data'].get('user_type', 'N/A')}")
        results["passed"] += 1
    else:
        results["failed"] += 1

    # Test 3: Password Mismatch Validation
    print_test(3, "Password Mismatch Validation (Should Fail)")
    resp = requests.post(
        f"{BASE_URL}/api/v1/auth_app/signup",
        json={
            "email_address": "error@test.com",
            "password": "Test@1234",
            "password2": "Different@1234",
            "first_name": "Test",
            "last_name": "User",
            "user_type": "STUDENT",
        },
    )
    if print_result(resp.status_code, 400, "Correctly rejected mismatched passwords"):
        results["passed"] += 1
    else:
        results["failed"] += 1

    # Test 4: Student Login
    print_test(4, "Student Login")
    student_email = f"logintest_student_{datetime.now().timestamp()}@test.com"
    # First create student
    requests.post(
        f"{BASE_URL}/api/v1/auth_app/signup",
        json={
            "email_address": student_email,
            "password": "Test@1234",
            "password2": "Test@1234",
            "first_name": "Login",
            "last_name": "Test",
            "user_type": "STUDENT",
        },
    )
    # Then login
    resp = requests.post(
        f"{BASE_URL}/api/v1/auth_app/login",
        json={"email_address": student_email, "password": "Test@1234"},
    )
    if print_result(resp.status_code, 200):
        login_data = resp.json()
        student_token = login_data.get("access")
        student_refresh = login_data.get("refresh")
        print(f"   Token: {student_token[:50] if student_token else 'N/A'}...")
        print(f"   User Type: {login_data.get('user_type', 'N/A')}")
        results["passed"] += 1
    else:
        results["failed"] += 1
        student_token = None
        student_refresh = None

    # Test 5: Instructor Login
    print_test(5, "Instructor Login")
    resp = requests.post(
        f"{BASE_URL}/api/v1/auth_app/login",
        json={"email_address": instructor_email, "password": "Test@1234"},
    )
    if print_result(resp.status_code, 200):
        login_data = resp.json()
        instructor_token = login_data.get("access")
        print(f"   Token: {instructor_token[:50] if instructor_token else 'N/A'}...")
        print(f"   User Type: {login_data.get('user_type', 'N/A')}")
        results["passed"] += 1
    else:
        results["failed"] += 1
        instructor_token = None

    # Test 6: Token Refresh
    if student_refresh:
        print_test(6, "Token Refresh")
        resp = requests.post(
            f"{BASE_URL}/api/v1/auth_app/token/refresh",
            json={"refresh": student_refresh},
        )
        if print_result(resp.status_code, 200, "New access token generated"):
            results["passed"] += 1
        else:
            results["failed"] += 1

    # Test 7: Instructor Creates Course
    if instructor_token:
        print_test(7, "Instructor Creates Course")
        resp = requests.post(
            f"{BASE_URL}/api/v1/course_app/courses/create",
            headers={"Authorization": f"Bearer {instructor_token}"},
            json={
                "title": f"Python Course {datetime.now().timestamp()}",
                "description": "Complete Python programming course",
            },
        )
        if print_result(resp.status_code, 201):
            course_data = resp.json()
            if "data" in course_data:
                print(f"   Title: {course_data['data'].get('title', 'N/A')}")
                # Try to get course_id from response
                course_id = course_data.get("data", {}).get("id")
                if not course_id:
                    # If not in response, we'll need to list courses
                    print("   Note: Course ID not in create response")
            results["passed"] += 1
        else:
            results["failed"] += 1
            print(f"   Error: {resp.text[:200]}")
            course_id = None
    else:
        course_id = None

    # Test 8: Student Cannot Create Course
    if student_token:
        print_test(8, "Student Cannot Create Course (Permission Test)")
        resp = requests.post(
            f"{BASE_URL}/api/v1/course_app/courses/create",
            headers={"Authorization": f"Bearer {student_token}"},
            json={"title": "Unauthorized Course", "description": "This should fail"},
        )
        if print_result(resp.status_code, 403, "Correctly denied permission"):
            results["passed"] += 1
        else:
            results["failed"] += 1
            print(f"   Unexpected response: {resp.text[:200]}")

    # Test 9: List Courses
    if student_token:
        print_test(9, "List Courses")
        resp = requests.get(
            f"{BASE_URL}/api/v1/course_app/courses/list",
            headers={"Authorization": f"Bearer {student_token}"},
        )
        if print_result(resp.status_code, 200):
            data = resp.json()
            courses = data.get("data", data.get("results", []))
            print(
                f"   Found {len(courses) if isinstance(courses, list) else 'N/A'} course(s)"
            )
            results["passed"] += 1
        else:
            results["failed"] += 1

    # Print Summary
    print_header("TEST SUMMARY")
    total = results["passed"] + results["failed"]
    print(f"\n   Total Tests: {total}")
    print(f"   ✅ Passed: {results['passed']}")
    print(f"   ❌ Failed: {results['failed']}")
    if total > 0:
        print(f"   Success Rate: {(results['passed'] / total) * 100:.1f}%")
    print(f"\n   Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n" + "=" * 70 + "\n")

    return results


if __name__ == "__main__":
    try:
        results = test_api()
        exit(0 if results["failed"] == 0 else 1)
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to server at http://localhost:8000")
        print("   Make sure the server is running (docker-compose up)")
        exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        exit(1)
