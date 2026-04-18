#!/usr/bin/env python3
"""
Test script for the POST /api/v1/generate endpoint.

Run this script to test the story generation API with various scenarios:
- Valid requests
- Invalid inputs
- Error handling

Usage:
    python test_endpoint.py
"""

import requests
import json
import sys
from typing import Dict, Any

# Configuration
API_BASE_URL = "http://localhost:8000/api/v1"
GENERATE_ENDPOINT = f"{API_BASE_URL}/generate"
HEALTH_ENDPOINT = f"{API_BASE_URL}/health"

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")


def print_test(test_name: str):
    """Print test name"""
    print(f"{Colors.OKCYAN}► {test_name}{Colors.ENDC}")


def print_success(message: str):
    """Print success message"""
    print(f"  {Colors.OKGREEN}✓ {message}{Colors.ENDC}")


def print_error(message: str):
    """Print error message"""
    print(f"  {Colors.FAIL}✗ {message}{Colors.ENDC}")


def print_info(message: str):
    """Print info message"""
    print(f"  {Colors.OKCYAN}ℹ {message}{Colors.ENDC}")


def check_server_health() -> bool:
    """Check if server is running"""
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=5)
        if response.status_code == 200:
            data = response.json()
            model_loaded = data.get("model_loaded", False)
            device = data.get("device", "unknown")
            
            print_success(f"Server is running")
            print_info(f"Model loaded: {model_loaded}")
            print_info(f"Device: {device}")
            
            if not model_loaded:
                print_error("Model is not loaded! Generation will fail.")
                return False
            
            return True
        else:
            print_error(f"Server returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error(f"Cannot connect to server at {API_BASE_URL}")
        print_info("Make sure the server is running:")
        print_info("  .\venv\\Scripts\\Activate.ps1")
        print_info("  uvicorn app.main:app --reload")
        return False
    except Exception as e:
        print_error(f"Error checking server: {str(e)}")
        return False


def test_valid_request():
    """Test with valid input"""
    print_test("Valid Request")
    
    payload = {
        "name": "Minh",
        "personality": "dũng cảm",
        "setting": "một ngôi làng ven biển",
        "theme": "phiêu lưu"
    }
    
    print_info(f"Request: {json.dumps(payload, ensure_ascii=False, indent=2)}")
    
    try:
        response = requests.post(GENERATE_ENDPOINT, json=payload, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Response received (200 OK)")
            print_info(f"Status: {data['status']}")
            print_info(f"Story: {data['story'][:100]}...")
            print_info(f"Message: {data.get('message', 'N/A')}")
            return True
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            print_info(f"Response: {response.text}")
            return False
    
    except requests.exceptions.Timeout:
        print_error("Request timed out (60s). Model generation took too long.")
        return False
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
        return False


def test_empty_name():
    """Test with empty name field"""
    print_test("Invalid Input: Empty Name")
    
    payload = {
        "name": "",
        "personality": "dũng cảm",
        "setting": "làng",
        "theme": "phiêu lưu"
    }
    
    try:
        response = requests.post(GENERATE_ENDPOINT, json=payload, timeout=10)
        
        if response.status_code == 400:
            print_success("Correctly returned 400 Bad Request")
            print_info(f"Error: {response.json()['detail']}")
            return True
        elif response.status_code == 422:
            print_success("Correctly returned 422 Unprocessable Entity (Pydantic validation)")
            print_info(f"Error: {response.json()['detail'][0]['msg']}")
            return True
        else:
            print_error(f"Expected 400 or 422, got {response.status_code}")
            return False
    
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
        return False


def test_missing_field():
    """Test with missing required field"""
    print_test("Invalid Input: Missing Field")
    
    payload = {
        "name": "Minh",
        "personality": "dũng cảm",
        "setting": "làng"
        # Missing 'theme'
    }
    
    try:
        response = requests.post(GENERATE_ENDPOINT, json=payload, timeout=10)
        
        if response.status_code == 422:
            print_success("Correctly returned 422 Unprocessable Entity")
            print_info(f"Error: Missing required field")
            return True
        else:
            print_error(f"Expected 422, got {response.status_code}")
            return False
    
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
        return False


def test_oversized_field():
    """Test with field exceeding max length"""
    print_test("Invalid Input: Field Too Long")
    
    payload = {
        "name": "A" * 101,  # Exceeds max_length of 100
        "personality": "dũng cảm",
        "setting": "làng",
        "theme": "phiêu lưu"
    }
    
    try:
        response = requests.post(GENERATE_ENDPOINT, json=payload, timeout=10)
        
        if response.status_code == 422:
            print_success("Correctly returned 422 Unprocessable Entity")
            print_info(f"Error: Field exceeds maximum length")
            return True
        else:
            print_error(f"Expected 422, got {response.status_code}")
            return False
    
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
        return False


def test_vietnamese_characters():
    """Test with various Vietnamese text"""
    print_test("Vietnamese Character Support")
    
    payload = {
        "name": "Nguyễn Thành",
        "personality": "thông minh, tốt bụng",
        "setting": "Sài Gòn, năm 1985",
        "theme": "tình yêu và hy vọng"
    }
    
    print_info(f"Request: {json.dumps(payload, ensure_ascii=False, indent=2)}")
    
    try:
        response = requests.post(GENERATE_ENDPOINT, json=payload, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Vietnamese characters handled correctly")
            print_info(f"Story: {data['story'][:100]}...")
            return True
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            return False
    
    except requests.exceptions.Timeout:
        print_error("Request timed out")
        return False
    except Exception as e:
        print_error(f"Request failed: {str(e)}")
        return False


def run_all_tests():
    """Run all tests"""
    print_header("Story Generation API Test Suite")
    
    # Check server health first
    print_test("Checking Server Health")
    if not check_server_health():
        print_error("Server is not available. Tests cancelled.")
        return False
    
    results = []
    
    # Run tests
    results.append(("Valid Request", test_valid_request()))
    results.append(("Empty Name Field", test_empty_name()))
    results.append(("Missing Field", test_missing_field()))
    results.append(("Field Too Long", test_oversized_field()))
    results.append(("Vietnamese Characters", test_vietnamese_characters()))
    
    # Print summary
    print_header("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{Colors.OKGREEN}✓ PASS{Colors.ENDC}" if result else f"{Colors.FAIL}✗ FAIL{Colors.ENDC}"
        print(f"  {status}  {test_name}")
    
    print()
    print(f"{Colors.BOLD}Results: {passed}/{total} tests passed{Colors.ENDC}")
    
    if passed == total:
        print(f"{Colors.OKGREEN}{Colors.BOLD}All tests passed! 🎉{Colors.ENDC}\n")
        return True
    else:
        print(f"{Colors.WARNING}{Colors.BOLD}Some tests failed. Check the output above.{Colors.ENDC}\n")
        return False


def test_single_request(name: str, personality: str, setting: str, theme: str):
    """Test a single request with custom parameters"""
    print_header(f"Single Request Test: {name}")
    
    payload = {
        "name": name,
        "personality": personality,
        "setting": setting,
        "theme": theme
    }
    
    print_info(f"Request payload:")
    print(f"  {json.dumps(payload, ensure_ascii=False, indent=2)}")
    
    try:
        print_info("Sending request to API...")
        response = requests.post(GENERATE_ENDPOINT, json=payload, timeout=60)
        
        print(f"\nStatus: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n{Colors.OKGREEN}✓ Success!{Colors.ENDC}")
            print(f"\nGenerated Story:")
            print(f"{Colors.OKCYAN}{data['story']}{Colors.ENDC}")
        else:
            print(f"\n{Colors.FAIL}✗ Error ({response.status_code}){Colors.ENDC}")
            print(f"Response: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    
    except requests.exceptions.Timeout:
        print(f"{Colors.FAIL}✗ Request timed out (60s){Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}✗ Error: {str(e)}{Colors.ENDC}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--single":
        # Single request mode
        if len(sys.argv) < 6:
            print("Usage: python test_endpoint.py --single <name> <personality> <setting> <theme>")
            sys.exit(1)
        
        name = sys.argv[2]
        personality = sys.argv[3]
        setting = sys.argv[4]
        theme = sys.argv[5]
        
        test_single_request(name, personality, setting, theme)
    else:
        # Full test suite
        success = run_all_tests()
        sys.exit(0 if success else 1)
