"""
Test suite for OpenBanking Services API Client

This module contains comprehensive tests for the Flask API that interacts
with OpenBanking Brasil mock API endpoints.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import requests
from app import create_app, OpenBankingClient, OpenBankingConfig, PaginationParams


class TestOpenBankingConfig(unittest.TestCase):
    """Test cases for OpenBankingConfig class."""
    
    def test_config_initialization(self):
        """Test config initialization with default values."""
        config = OpenBankingConfig()
        self.assertEqual(config.base_url, "http://localhost:7004/open-banking/products-services/v2")
        self.assertEqual(config.timeout, 30)
        self.assertIn('Content-Type', config.default_headers)
    
    def test_config_custom_base_url(self):
        """Test config initialization with custom base URL."""
        custom_url = "http://custom.example.com/api"
        config = OpenBankingConfig(custom_url)
        self.assertEqual(config.base_url, custom_url)


class TestPaginationParams(unittest.TestCase):
    """Test cases for PaginationParams Pydantic model."""
    
    def test_valid_pagination_params(self):
        """Test valid pagination parameters."""
        params = PaginationParams(page=1, page_size=25)
        self.assertEqual(params.page, 1)
        self.assertEqual(params.page_size, 25)
    
    def test_default_pagination_params(self):
        """Test default pagination parameters."""
        params = PaginationParams()
        self.assertEqual(params.page, 1)
        self.assertEqual(params.page_size, 25)


class TestOpenBankingClient(unittest.TestCase):
    """Test cases for OpenBankingClient class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config = OpenBankingConfig()
        self.client = OpenBankingClient(self.config)
    
    @patch.object(OpenBankingClient, '_make_request')
    def test_get_personal_accounts(self, mock_make_request):
        """Test get_personal_accounts method."""
        mock_make_request.return_value = {"data": "personal_accounts"}
        
        result = self.client.get_personal_accounts(page=1, page_size=10)
        
        mock_make_request.assert_called_once_with(
            "/personal-accounts", 
            {"page": 1, "page-size": 10}
        )
        self.assertEqual(result, {"data": "personal_accounts"})
    
    @patch.object(OpenBankingClient, '_make_request')
    def test_get_business_accounts(self, mock_make_request):
        """Test get_business_accounts method."""
        mock_make_request.return_value = {"data": "business_accounts"}
        
        result = self.client.get_business_accounts()
        
        mock_make_request.assert_called_once_with(
            "/business-accounts",
            {"page": 1, "page-size": 25}
        )
        self.assertEqual(result, {"data": "business_accounts"})
    
    @patch.object(OpenBankingClient, '_make_request')
    def test_all_endpoints(self, mock_make_request):
        """Test all client endpoint methods."""
        mock_make_request.return_value = {"data": "test"}
        
        endpoints = [
            ("get_personal_loans", "/personal-loans"),
            ("get_business_loans", "/business-loans"),
            ("get_personal_credit_cards", "/personal-credit-cards"),
            ("get_business_credit_cards", "/business-credit-cards"),
            ("get_personal_financings", "/personal-financings"),
            ("get_business_financings", "/business-financings"),
            ("get_personal_invoice_financings", "/personal-invoice-financings"),
            ("get_business_invoice_financings", "/business-invoice-financings"),
            ("get_personal_unarranged_account_overdraft", "/personal-unarranged-account-overdraft"),
            ("get_business_unarranged_account_overdraft", "/business-unarranged-account-overdraft")
        ]
        
        for method_name, endpoint_path in endpoints:
            with self.subTest(method=method_name):
                mock_make_request.reset_mock()
                method = getattr(self.client, method_name)
                result = method()
                
                mock_make_request.assert_called_once_with(
                    endpoint_path,
                    {"page": 1, "page-size": 25}
                )
                self.assertEqual(result, {"data": "test"})


class TestFlaskAPI(unittest.TestCase):
    """Test cases for Flask API endpoints."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['service'], 'openbanking-api-client')
    
    def test_list_endpoints(self):
        """Test endpoints listing."""
        response = self.client.get('/api/v1/endpoints')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('endpoints', data)
        self.assertIsInstance(data['endpoints'], list)
        self.assertTrue(len(data['endpoints']) > 0)
    
    def test_not_found_endpoint(self):
        """Test 404 error handling."""
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    @patch('app.OpenBankingClient.get_personal_accounts')
    def test_personal_accounts_endpoint(self, mock_get_personal_accounts):
        """Test personal accounts endpoint."""
        mock_get_personal_accounts.return_value = {"data": "personal_accounts"}
        
        response = self.client.get('/api/v1/personal-accounts')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data, {"data": "personal_accounts"})
        mock_get_personal_accounts.assert_called_once()
    
    @patch('app.OpenBankingClient.get_personal_accounts')
    def test_personal_accounts_with_pagination(self, mock_get_personal_accounts):
        """Test personal accounts endpoint with pagination."""
        mock_get_personal_accounts.return_value = {"data": "personal_accounts"}
        
        response = self.client.get('/api/v1/personal-accounts?page=2&page-size=50')
        self.assertEqual(response.status_code, 200)
        
        mock_get_personal_accounts.assert_called_once_with(2, 50)
    
    @patch('app.OpenBankingClient.get_business_accounts')
    def test_business_accounts_endpoint(self, mock_get_business_accounts):
        """Test business accounts endpoint."""
        mock_get_business_accounts.return_value = {"data": "business_accounts"}
        
        response = self.client.get('/api/v1/business-accounts')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data, {"data": "business_accounts"})
    
    @patch('app.OpenBankingClient._make_request')
    def test_api_error_handling(self, mock_make_request):
        """Test API error handling."""
        mock_make_request.side_effect = requests.exceptions.RequestException("API Error")
        
        response = self.client.get('/api/v1/personal-accounts')
        self.assertEqual(response.status_code, 502)
        
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'External API request failed')
    
    def test_all_api_endpoints(self):
        """Test all API endpoints exist and return proper structure."""
        endpoints = [
            '/api/v1/personal-accounts',
            '/api/v1/business-accounts',
            '/api/v1/personal-loans',
            '/api/v1/business-loans',
            '/api/v1/personal-credit-cards',
            '/api/v1/business-credit-cards',
            '/api/v1/personal-financings',
            '/api/v1/business-financings',
            '/api/v1/personal-invoice-financings',
            '/api/v1/business-invoice-financings',
            '/api/v1/personal-unarranged-account-overdraft',
            '/api/v1/business-unarranged-account-overdraft'
        ]
        
        for endpoint in endpoints:
            with self.subTest(endpoint=endpoint):
                # Since we can't connect to actual mock API in tests,
                # we expect 502 error which indicates the endpoint exists
                # but external API is unavailable
                response = self.client.get(endpoint)
                self.assertIn(response.status_code, [200, 502])


class TestIntegration(unittest.TestCase):
    """Integration tests (require mock API to be running)."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    @unittest.skip("Requires mock API to be running")
    def test_integration_personal_accounts(self):
        """Test integration with actual mock API for personal accounts."""
        response = self.client.get('/api/v1/personal-accounts')
        
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIn('data', data)
            self.assertIn('links', data)
            self.assertIn('meta', data)
        else:
            # Mock API not available, skip test
            self.skipTest("Mock API not available")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
