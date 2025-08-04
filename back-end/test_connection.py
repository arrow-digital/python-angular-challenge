#!/usr/bin/env python3
"""
OpenBanking API Client Test Script

This script tests the connection to the mock API and validates
that all endpoints are working correctly.
"""

import requests
import json
import sys
from typing import Dict, Any, List


class APITester:
    """Test class for validating API endpoints."""
    
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.mock_api_url = "http://localhost:7004/open-banking/products-services/v2"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def test_mock_api_connection(self) -> bool:
        """Test if the mock API is running."""
        try:
            # Try to connect to one of the mock API endpoints
            response = self.session.get(
                f"{self.mock_api_url}/personal-accounts",
                timeout=5
            )
            print(f"Mock API is running (Status: {response.status_code})")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Mock API is not running: {str(e)}")
            print("Please start the mock API with: cd mock-api && docker-compose up")
            return False
    
    def test_flask_api_connection(self) -> bool:
        """Test if the Flask API is running."""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"Flask API is running: {data.get('service', 'unknown')}")
                return True
            else:
                print(f"Flask API returned status: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Flask API is not running: {str(e)}")
            print("Please start the Flask API with: python app.py")
            return False
    
    def test_endpoint(self, endpoint: str, expected_keys: List[str] = None) -> bool:
        """Test a specific API endpoint."""
        if expected_keys is None:
            expected_keys = ['data', 'links', 'meta']
        
        try:
            url = f"{self.base_url}/api/v1/{endpoint}"
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check if response has expected structure
                missing_keys = [key for key in expected_keys if key not in data]
                if missing_keys:
                    print(f"{endpoint}: Missing keys {missing_keys}")
                    return False
                
                print(f"{endpoint}: OK")
                return True
                
            elif response.status_code == 502:
                print(f"{endpoint}: External API unavailable (502)")
                return False
                
            else:
                print(f"{endpoint}: HTTP {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"{endpoint}: {str(e)}")
            return False
    
    def test_all_endpoints(self) -> Dict[str, bool]:
        """Test all available endpoints."""
        endpoints = [
            'personal-accounts',
            'business-accounts',
            'personal-loans',
            'business-loans',
            'personal-credit-cards',
            'business-credit-cards',
            'personal-financings',
            'business-financings',
            'personal-invoice-financings',
            'business-invoice-financings',
            'personal-unarranged-account-overdraft',
            'business-unarranged-account-overdraft'
        ]
        
        results = {}
        print("\nTesting all endpoints...")
        print("-" * 50)
        
        for endpoint in endpoints:
            results[endpoint] = self.test_endpoint(endpoint)
        
        return results
    
    def test_pagination(self) -> bool:
        """Test pagination functionality."""
        try:
            url = f"{self.base_url}/api/v1/personal-accounts"
            params = {'page': 1, 'page-size': 10}
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code in [200, 502]:  # 502 if mock API unavailable
                print("Pagination: Parameters accepted")
                return True
            else:
                print(f"Pagination: HTTP {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"Pagination: {str(e)}")
            return False
    
    def test_error_handling(self) -> bool:
        """Test error handling for invalid endpoints."""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/nonexistent")
            
            if response.status_code == 404:
                print("Error handling: 404 for invalid endpoint")
                return True
            else:
                print(f"Error handling: Expected 404, got {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"Error handling: {str(e)}")
            return False
    
    def run_full_test_suite(self) -> None:
        """Run the complete test suite."""
        print("OpenBanking API Client Test Suite")
        print("=" * 50)
        
        # Test connections
        print("\n🔗 Testing Connections...")
        mock_api_ok = self.test_mock_api_connection()
        flask_api_ok = self.test_flask_api_connection()
        
        if not flask_api_ok:
            print("\nCannot continue tests - Flask API not running")
            sys.exit(1)
        
        # Test endpoints
        endpoint_results = self.test_all_endpoints()
        
        # Test pagination
        print("\nTesting Pagination...")
        pagination_ok = self.test_pagination()
        
        # Test error handling
        print("\nTesting Error Handling...")
        error_handling_ok = self.test_error_handling()
        
        # Summary
        print("\nTest Summary")
        print("=" * 50)
        
        total_endpoints = len(endpoint_results)
        successful_endpoints = sum(endpoint_results.values())
        
        print(f"Mock API Connection: {'✅' if mock_api_ok else '❌'}")
        print(f"Flask API Connection: {'✅' if flask_api_ok else '❌'}")
        print(f"Endpoints: {successful_endpoints}/{total_endpoints} working")
        print(f"Pagination: {'✅' if pagination_ok else '❌'}")
        print(f"Error Handling: {'✅' if error_handling_ok else '❌'}")
        
        if not mock_api_ok:
            print("\nNote: Some endpoints may fail because mock API is not running")
            print("   Start with: cd mock-api && docker-compose up")
        
        # Overall status
        if successful_endpoints == total_endpoints and pagination_ok and error_handling_ok:
            print("\nAll tests passed!")
            sys.exit(0)
        else:
            print("\nSome tests failed - check output above")
            sys.exit(1)


def main():
    """Main function to run the test suite."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test OpenBanking API Client')
    parser.add_argument(
        '--url', 
        default='http://localhost:5000',
        help='Base URL of the Flask API (default: http://localhost:5000)'
    )
    parser.add_argument(
        '--endpoint',
        help='Test a specific endpoint only'
    )
    
    args = parser.parse_args()
    
    tester = APITester(args.url)
    
    if args.endpoint:
        # Test specific endpoint
        print(f"Testing endpoint: {args.endpoint}")
        success = tester.test_endpoint(args.endpoint)
        sys.exit(0 if success else 1)
    else:
        # Run full test suite
        tester.run_full_test_suite()


if __name__ == '__main__':
    main()
