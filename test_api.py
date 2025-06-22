#!/usr/bin/env python3
"""
Test script for Organization Management API
Run this after starting the application to test the endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code} - {response.json()}")
    return response.status_code == 200

def test_create_organization():
    """Test organization creation"""
    print("\nTesting organization creation...")
    
    org_data = {
        "email": "admin@testcorp.com",
        "password": "securepassword123",
        "organization_name": "Test Corporation"
    }
    
    response = requests.post(f"{BASE_URL}/org/create", json=org_data)
    print(f"Create organization: {response.status_code}")
    
    if response.status_code == 201:
        org = response.json()
        print(f"Organization created: {org['name']} (ID: {org['id']})")
        return org
    else:
        print(f"Error: {response.text}")
        return None

def test_get_organization(org_name):
    """Test getting organization by name"""
    print(f"\nTesting get organization: {org_name}")
    
    response = requests.get(f"{BASE_URL}/org/get", params={"organization_name": org_name})
    print(f"Get organization: {response.status_code}")
    
    if response.status_code == 200:
        org = response.json()
        print(f"Organization found: {org['name']} (ID: {org['id']})")
        return org
    else:
        print(f"Error: {response.text}")
        return None

def test_admin_login(email, password):
    """Test admin login"""
    print(f"\nTesting admin login: {email}")
    
    login_data = {
        "email": email,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/admin/login", json=login_data)
    print(f"Admin login: {response.status_code}")
    
    if response.status_code == 200:
        token_data = response.json()
        print(f"Login successful: {token_data['user_email']}")
        print(f"Token: {token_data['access_token'][:50]}...")
        return token_data
    else:
        print(f"Error: {response.text}")
        return None

def test_admin_me(token):
    """Test getting current admin info"""
    print("\nTesting admin/me endpoint...")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/admin/me", headers=headers)
    print(f"Admin me: {response.status_code}")
    
    if response.status_code == 200:
        admin_info = response.json()
        print(f"Admin info: {admin_info}")
        return admin_info
    else:
        print(f"Error: {response.text}")
        return None

def main():
    """Run all tests"""
    print("=== Organization Management API Test ===")
    
    # Test health
    if not test_health():
        print("Health check failed. Make sure the application is running.")
        return
    
    # Test organization creation
    org = test_create_organization()
    if not org:
        print("Organization creation failed.")
        return
    
    # Test get organization
    test_get_organization(org['name'])
    
    # Test admin login
    token_data = test_admin_login(org['email'], "securepassword123")
    if not token_data:
        print("Admin login failed.")
        return
    
    # Test admin/me endpoint
    test_admin_me(token_data['access_token'])
    
    print("\n=== All tests completed ===")

if __name__ == "__main__":
    main() 