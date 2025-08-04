"""
OpenBanking Services API Client

A Flask API that interacts with OpenBanking Brasil mock API endpoints.
This module provides a RESTful interface to consume all OpenBanking services
following PEP8 standards.

Author: Python Challenge
Version: 1.0.0
"""

import logging
from typing import Dict, Any, Optional
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import requests
from pydantic import BaseModel, ValidationError


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
BASE_URL = "http://localhost:7004/open-banking/products-services/v2"
DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 25


class OpenBankingConfig:
    """Configuration class for OpenBanking API settings."""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.timeout = 30
        self.default_headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }


class PaginationParams(BaseModel):
    """Pydantic model for pagination parameters validation."""
    
    page: int = DEFAULT_PAGE
    page_size: int = DEFAULT_PAGE_SIZE
    
    class Config:
        """Pydantic configuration."""
        validate_assignment = True
        extra = "forbid"


class OpenBankingClient:
    """Client class for interacting with OpenBanking API endpoints."""
    
    def __init__(self, config: OpenBankingConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update(config.default_headers)
    
    def _make_request(
        self, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to OpenBanking API.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            JSON response data
            
        Raises:
            requests.RequestException: If request fails
        """
        url = f"{self.config.base_url}{endpoint}"
        
        try:
            logger.info(f"Making request to: {url} with params: {params}")
            response = self.session.get(
                url,
                params=params,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as exc:
            logger.error(f"Request failed for {url}: {str(exc)}")
            raise
    
    def get_personal_accounts(
        self, 
        page: int = DEFAULT_PAGE, 
        page_size: int = DEFAULT_PAGE_SIZE
    ) -> Dict[str, Any]:
        """Get personal accounts data."""
        params = {"page": page, "page-size": page_size}
        return self._make_request("/personal-accounts", params)
    
    def get_business_accounts(
        self, 
        page: int = DEFAULT_PAGE, 
        page_size: int = DEFAULT_PAGE_SIZE
    ) -> Dict[str, Any]:
        """Get business accounts data."""
        params = {"page": page, "page-size": page_size}
        return self._make_request("/business-accounts", params)
    
    def get_personal_loans(
        self, 
        page: int = DEFAULT_PAGE, 
        page_size: int = DEFAULT_PAGE_SIZE
    ) -> Dict[str, Any]:
        """Get personal loans data."""
        params = {"page": page, "page-size": page_size}
        return self._make_request("/personal-loans", params)
    
    def get_business_loans(
        self, 
        page: int = DEFAULT_PAGE, 
        page_size: int = DEFAULT_PAGE_SIZE
    ) -> Dict[str, Any]:
        """Get business loans data."""
        params = {"page": page, "page-size": page_size}
        return self._make_request("/business-loans", params)
    
    def get_personal_credit_cards(
        self, 
        page: int = DEFAULT_PAGE, 
        page_size: int = DEFAULT_PAGE_SIZE
    ) -> Dict[str, Any]:
        """Get personal credit cards data."""
        params = {"page": page, "page-size": page_size}
        return self._make_request("/personal-credit-cards", params)
    
    def get_business_credit_cards(
        self, 
        page: int = DEFAULT_PAGE, 
        page_size: int = DEFAULT_PAGE_SIZE
    ) -> Dict[str, Any]:
        """Get business credit cards data."""
        params = {"page": page, "page-size": page_size}
        return self._make_request("/business-credit-cards", params)
    
    def get_personal_financings(
        self, 
        page: int = DEFAULT_PAGE, 
        page_size: int = DEFAULT_PAGE_SIZE
    ) -> Dict[str, Any]:
        """Get personal financings data."""
        params = {"page": page, "page-size": page_size}
        return self._make_request("/personal-financings", params)
    
    def get_business_financings(
        self, 
        page: int = DEFAULT_PAGE, 
        page_size: int = DEFAULT_PAGE_SIZE
    ) -> Dict[str, Any]:
        """Get business financings data."""
        params = {"page": page, "page-size": page_size}
        return self._make_request("/business-financings", params)
    
    def get_personal_invoice_financings(
        self, 
        page: int = DEFAULT_PAGE, 
        page_size: int = DEFAULT_PAGE_SIZE
    ) -> Dict[str, Any]:
        """Get personal invoice financings data."""
        params = {"page": page, "page-size": page_size}
        return self._make_request("/personal-invoice-financings", params)
    
    def get_business_invoice_financings(
        self, 
        page: int = DEFAULT_PAGE, 
        page_size: int = DEFAULT_PAGE_SIZE
    ) -> Dict[str, Any]:
        """Get business invoice financings data."""
        params = {"page": page, "page-size": page_size}
        return self._make_request("/business-invoice-financings", params)
    
    def get_personal_unarranged_account_overdraft(
        self, 
        page: int = DEFAULT_PAGE, 
        page_size: int = DEFAULT_PAGE_SIZE
    ) -> Dict[str, Any]:
        """Get personal unarranged account overdraft data."""
        params = {"page": page, "page-size": page_size}
        return self._make_request("/personal-unarranged-account-overdraft", params)
    
    def get_business_unarranged_account_overdraft(
        self, 
        page: int = DEFAULT_PAGE, 
        page_size: int = DEFAULT_PAGE_SIZE
    ) -> Dict[str, Any]:
        """Get business unarranged account overdraft data."""
        params = {"page": page, "page-size": page_size}
        return self._make_request("/business-unarranged-account-overdraft", params)


def create_app() -> Flask:
    """Create and configure Flask application."""
    app = Flask(__name__)
    CORS(app)
    
    # Initialize OpenBanking client
    config = OpenBankingConfig()
    client = OpenBankingClient(config)
    
    def _validate_pagination_params() -> PaginationParams:
        """Validate and extract pagination parameters from request."""
        try:
            page = int(request.args.get('page', DEFAULT_PAGE))
            page_size = int(request.args.get('page-size', DEFAULT_PAGE_SIZE))
            return PaginationParams(page=page, page_size=page_size)
        except (ValueError, ValidationError) as exc:
            logger.error(f"Invalid pagination parameters: {str(exc)}")
            raise ValueError("Invalid pagination parameters")
    
    def _handle_api_error(func):
        """Decorator to handle API errors consistently."""
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ValueError as exc:
                return jsonify({"error": str(exc)}), 400
            except requests.exceptions.RequestException as exc:
                logger.error(f"API request failed: {str(exc)}")
                return jsonify({"error": "External API request failed"}), 502
            except Exception as exc:
                logger.error(f"Unexpected error: {str(exc)}")
                return jsonify({"error": "Internal server error"}), 500
        
        wrapper.__name__ = func.__name__
        return wrapper
    
    @app.route('/health', methods=['GET'])
    def health_check() -> Response:
        """Health check endpoint."""
        return jsonify({
            "status": "healthy",
            "service": "openbanking-api-client",
            "version": "1.0.0"
        })
    
    @app.route('/api/v1/personal-accounts', methods=['GET'])
    @_handle_api_error
    def get_personal_accounts() -> Response:
        """Get personal accounts data."""
        params = _validate_pagination_params()
        data = client.get_personal_accounts(params.page, params.page_size)
        return jsonify(data)
    
    @app.route('/api/v1/business-accounts', methods=['GET'])
    @_handle_api_error
    def get_business_accounts() -> Response:
        """Get business accounts data."""
        params = _validate_pagination_params()
        data = client.get_business_accounts(params.page, params.page_size)
        return jsonify(data)
    
    @app.route('/api/v1/personal-loans', methods=['GET'])
    @_handle_api_error
    def get_personal_loans() -> Response:
        """Get personal loans data."""
        params = _validate_pagination_params()
        data = client.get_personal_loans(params.page, params.page_size)
        return jsonify(data)
    
    @app.route('/api/v1/business-loans', methods=['GET'])
    @_handle_api_error
    def get_business_loans() -> Response:
        """Get business loans data."""
        params = _validate_pagination_params()
        data = client.get_business_loans(params.page, params.page_size)
        return jsonify(data)
    
    @app.route('/api/v1/personal-credit-cards', methods=['GET'])
    @_handle_api_error
    def get_personal_credit_cards() -> Response:
        """Get personal credit cards data."""
        params = _validate_pagination_params()
        data = client.get_personal_credit_cards(params.page, params.page_size)
        return jsonify(data)
    
    @app.route('/api/v1/business-credit-cards', methods=['GET'])
    @_handle_api_error
    def get_business_credit_cards() -> Response:
        """Get business credit cards data."""
        params = _validate_pagination_params()
        data = client.get_business_credit_cards(params.page, params.page_size)
        return jsonify(data)
    
    @app.route('/api/v1/personal-financings', methods=['GET'])
    @_handle_api_error
    def get_personal_financings() -> Response:
        """Get personal financings data."""
        params = _validate_pagination_params()
        data = client.get_personal_financings(params.page, params.page_size)
        return jsonify(data)
    
    @app.route('/api/v1/business-financings', methods=['GET'])
    @_handle_api_error
    def get_business_financings() -> Response:
        """Get business financings data."""
        params = _validate_pagination_params()
        data = client.get_business_financings(params.page, params.page_size)
        return jsonify(data)
    
    @app.route('/api/v1/personal-invoice-financings', methods=['GET'])
    @_handle_api_error
    def get_personal_invoice_financings() -> Response:
        """Get personal invoice financings data."""
        params = _validate_pagination_params()
        data = client.get_personal_invoice_financings(params.page, params.page_size)
        return jsonify(data)
    
    @app.route('/api/v1/business-invoice-financings', methods=['GET'])
    @_handle_api_error
    def get_business_invoice_financings() -> Response:
        """Get business invoice financings data."""
        params = _validate_pagination_params()
        data = client.get_business_invoice_financings(params.page, params.page_size)
        return jsonify(data)
    
    @app.route('/api/v1/personal-unarranged-account-overdraft', methods=['GET'])
    @_handle_api_error
    def get_personal_unarranged_account_overdraft() -> Response:
        """Get personal unarranged account overdraft data."""
        params = _validate_pagination_params()
        data = client.get_personal_unarranged_account_overdraft(
            params.page, 
            params.page_size
        )
        return jsonify(data)
    
    @app.route('/api/v1/business-unarranged-account-overdraft', methods=['GET'])
    @_handle_api_error
    def get_business_unarranged_account_overdraft() -> Response:
        """Get business unarranged account overdraft data."""
        params = _validate_pagination_params()
        data = client.get_business_unarranged_account_overdraft(
            params.page, 
            params.page_size
        )
        return jsonify(data)
    
    @app.route('/api/v1/endpoints', methods=['GET'])
    def list_available_endpoints() -> Response:
        """List all available API endpoints."""
        endpoints = [
            {
                "path": "/api/v1/personal-accounts",
                "method": "GET",
                "description": "Get personal accounts data",
                "parameters": ["page", "page-size"]
            },
            {
                "path": "/api/v1/business-accounts", 
                "method": "GET",
                "description": "Get business accounts data",
                "parameters": ["page", "page-size"]
            },
            {
                "path": "/api/v1/personal-loans",
                "method": "GET", 
                "description": "Get personal loans data",
                "parameters": ["page", "page-size"]
            },
            {
                "path": "/api/v1/business-loans",
                "method": "GET",
                "description": "Get business loans data", 
                "parameters": ["page", "page-size"]
            },
            {
                "path": "/api/v1/personal-credit-cards",
                "method": "GET",
                "description": "Get personal credit cards data",
                "parameters": ["page", "page-size"]
            },
            {
                "path": "/api/v1/business-credit-cards",
                "method": "GET",
                "description": "Get business credit cards data",
                "parameters": ["page", "page-size"]
            },
            {
                "path": "/api/v1/personal-financings",
                "method": "GET",
                "description": "Get personal financings data",
                "parameters": ["page", "page-size"]
            },
            {
                "path": "/api/v1/business-financings",
                "method": "GET",
                "description": "Get business financings data",
                "parameters": ["page", "page-size"]
            },
            {
                "path": "/api/v1/personal-invoice-financings",
                "method": "GET",
                "description": "Get personal invoice financings data",
                "parameters": ["page", "page-size"]
            },
            {
                "path": "/api/v1/business-invoice-financings",
                "method": "GET",
                "description": "Get business invoice financings data",
                "parameters": ["page", "page-size"]
            },
            {
                "path": "/api/v1/personal-unarranged-account-overdraft",
                "method": "GET",
                "description": "Get personal unarranged account overdraft data",
                "parameters": ["page", "page-size"]
            },
            {
                "path": "/api/v1/business-unarranged-account-overdraft",
                "method": "GET",
                "description": "Get business unarranged account overdraft data",
                "parameters": ["page", "page-size"]
            }
        ]
        
        return jsonify({
            "service": "OpenBanking API Client",
            "version": "1.0.0",
            "base_url": config.base_url,
            "endpoints": endpoints
        })
    
    @app.errorhandler(404)
    def not_found(error) -> Response:
        """Handle 404 errors."""
        return jsonify({
            "error": "Endpoint not found",
            "message": "The requested endpoint does not exist"
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error) -> Response:
        """Handle 500 errors."""
        return jsonify({
            "error": "Internal server error",
            "message": "An unexpected error occurred"
        }), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    logger.info("Starting OpenBanking API Client")
    app.run(host='0.0.0.0', port=5000, debug=True)
