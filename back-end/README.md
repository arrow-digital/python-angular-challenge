# OpenBanking Services API Client

A Python Flask API client that interacts with OpenBanking Brasil mock API endpoints, following PEP8 specifications and best practices.

## Overview

This application provides a RESTful API interface to consume all OpenBanking Brasil services. It acts as a proxy/client that connects to the mock API running on `localhost:7004` and exposes clean, well-documented endpoints.

## Features

- ✅ Complete implementation of all OpenBanking Brasil endpoints
- ✅ PEP8 compliant code with comprehensive documentation
- ✅ Robust error handling and logging
- ✅ Input validation using Pydantic models
- ✅ Comprehensive test suite
- ✅ CORS support for web applications
- ✅ Pagination support
- ✅ Health check endpoint
- ✅ Configuration management
- ✅ Production-ready structure

## Available Endpoints

### Health & Information
- `GET /health` - Health check endpoint
- `GET /api/v1/endpoints` - List all available endpoints

### Accounts
- `GET /api/v1/personal-accounts` - Get personal accounts data
- `GET /api/v1/business-accounts` - Get business accounts data

### Loans
- `GET /api/v1/personal-loans` - Get personal loans data
- `GET /api/v1/business-loans` - Get business loans data

### Credit Cards
- `GET /api/v1/personal-credit-cards` - Get personal credit cards data
- `GET /api/v1/business-credit-cards` - Get business credit cards data

### Financings
- `GET /api/v1/personal-financings` - Get personal financings data
- `GET /api/v1/business-financings` - Get business financings data

### Invoice Financings
- `GET /api/v1/personal-invoice-financings` - Get personal invoice financings data
- `GET /api/v1/business-invoice-financings` - Get business invoice financings data

### Unarranged Account Overdraft
- `GET /api/v1/personal-unarranged-account-overdraft` - Get personal unarranged account overdraft data
- `GET /api/v1/business-unarranged-account-overdraft` - Get business unarranged account overdraft data

## Installation & Setup

### Prerequisites
- Python 3.8+
- Docker (for running the mock API)
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd python-challenge
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the Mock API
Navigate to the mock-api directory and start the Docker containers:

```bash
cd mock-api
docker-compose up
```

This will start the OpenBanking mock API on `localhost:7004`.

### 4. Start the Flask Application
```bash
python app.py
```

The API will be available at `http://localhost:5000`.

## Usage Examples

### Health Check
```bash
curl http://localhost:5000/health
```

### Get Personal Accounts
```bash
curl http://localhost:5000/api/v1/personal-accounts
```

### Get Personal Accounts with Pagination
```bash
curl "http://localhost:5000/api/v1/personal-accounts?page=1&page-size=10"
```

### List All Available Endpoints
```bash
curl http://localhost:5000/api/v1/endpoints
```

## Configuration

The application can be configured using environment variables:

```bash
export OPENBANKING_BASE_URL="http://localhost:7004/open-banking/products-services/v2"
export FLASK_ENV="development"
export LOG_LEVEL="INFO"
export DEFAULT_PAGE_SIZE="25"
export MAX_PAGE_SIZE="100"
```

## Testing

Run the test suite:

```bash
python -m pytest test_app.py -v
```

Or using unittest:

```bash
python test_app.py
```

## Project Structure

```
python-challenge/
├── app.py                 # Main Flask application
├── config.py             # Configuration management
├── test_app.py           # Comprehensive test suite
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── openbanking-services.yaml  # OpenAPI specification
└── mock-api/            # Mock API Docker setup
    ├── docker-compose.yml
    ├── Dockerfile
    └── README.md
```

## API Response Format

All endpoints return JSON responses in the OpenBanking Brasil standard format:

```json
{
  "data": {
    "brand": {
      "name": "Organization Name",
      "companies": [...]
    }
  },
  "links": {
    "self": "https://api.banco.com.br/open-banking/products-services/v2/resource",
    "first": "https://api.banco.com.br/open-banking/products-services/v2/resource",
    "prev": null,
    "next": null,
    "last": "https://api.banco.com.br/open-banking/products-services/v2/resource"
  },
  "meta": {
    "totalRecords": 1,
    "totalPages": 1
  }
}
```

## Error Handling

The API provides consistent error responses:

```json
{
  "error": "Error description",
  "message": "Detailed error message"
}
```

Common HTTP status codes:
- `200` - Success
- `400` - Bad Request (invalid parameters)
- `404` - Not Found
- `502` - Bad Gateway (external API error)
- `500` - Internal Server Error

## PEP8 Compliance

This project follows PEP8 standards:
- Maximum line length: 88 characters (Black formatter standard)
- Proper import organization
- Consistent naming conventions
- Comprehensive docstrings
- Type hints where appropriate

## Development

### Code Style
The project uses:
- PEP8 for Python code style
- Type hints for better code documentation
- Docstrings for all public methods
- Comprehensive error handling

### Adding New Endpoints
1. Add the method to `OpenBankingClient` class
2. Add the Flask route in `create_app()` function
3. Add tests in `test_app.py`
4. Update this README

## Logging

The application uses Python's built-in logging module with configurable levels:
- DEBUG: Detailed information for debugging
- INFO: General information about application flow
- WARNING: Warning messages
- ERROR: Error messages

Logs include timestamps, module names, and detailed messages for troubleshooting.

## Security Considerations

- Input validation using Pydantic models
- CORS configuration for cross-origin requests
- Request timeouts to prevent hanging connections
- Comprehensive error handling to prevent information leakage

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes following PEP8 standards
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For questions or issues, please create an issue in the repository or contact the development team.
