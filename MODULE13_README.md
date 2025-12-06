# Module 13: JWT Authentication with Client-Side Validation & Playwright E2E Testing

## Overview

This module implements JWT-based authentication with front-end registration and login pages, complete with client-side validation and comprehensive Playwright E2E tests.

## Features

### ✅ JWT Authentication
- **Registration Endpoint** (`/users/register`): Creates new users with hashed passwords
- **Login Endpoint** (`/users/login`): Authenticates users and returns JWT tokens
- **Pydantic Validation**: Ensures data integrity and security
- **Duplicate Detection**: Prevents duplicate usernames and emails

### ✅ Front-End Pages
- **register.html**: User registration with email/password validation
  - Email format validation
  - Password minimum length (8 characters)
  - Password confirmation matching
  - JWT token storage in localStorage
  
- **login.html**: User authentication
  - Username/password validation
  - JWT token storage on successful login
  - Error handling for invalid credentials

### ✅ Playwright E2E Tests
- **Positive Tests**:
  - Successful registration with valid data
  - Successful login with correct credentials
  - JWT token storage verification
  
- **Negative Tests**:
  - Registration with short password
  - Registration with invalid email format
  - Registration with mismatched passwords
  - Login with wrong password
  - Login with nonexistent user

### ✅ CI/CD Pipeline
- Automated unit tests with pytest
- Playwright E2E tests in GitHub Actions
- Docker image build and push to Docker Hub
- PostgreSQL database service for testing

## Installation

### Prerequisites
- Python 3.11+
- PostgreSQL (or SQLite for local development)
- Docker (optional, for containerized deployment)

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ashika2031/fast_api_calculator.git
   cd fast_api_calculator
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright Browsers**
   ```bash
   playwright install chromium
   ```

5. **Configure Environment Variables**
   Create a `.env` file:
   ```env
   DATABASE_URL=sqlite:///./calculator.db
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

## Running the Application

### Start the Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Access the Application
- **API Documentation**: http://localhost:8000/docs
- **Registration Page**: http://localhost:8000/static/register.html
- **Login Page**: http://localhost:8000/static/login.html
- **Demo UI**: http://localhost:8000/static/index.html

## Running Tests

### Unit Tests
```bash
# Run all unit tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=term

# Run specific test file
pytest tests/test_users.py -v
```

### Playwright E2E Tests
```bash
# Run all E2E tests
pytest e2e/ -v --browser chromium

# Run in headed mode (see browser)
pytest e2e/ -v --browser chromium --headed

# Run specific test
pytest e2e/test_auth_e2e.py::TestRegistration::test_register_with_valid_data -v

# Run with screenshots on failure
pytest e2e/ -v --screenshot on --video on
```

### Run All Tests
```bash
# Unit tests + E2E tests
pytest -v
```

## Docker Deployment

### Build Docker Image
```bash
docker build -t fastapi-calculator .
```

### Run with Docker Compose
```bash
docker-compose up -d
```

### Access Dockerized App
- API: http://localhost:8000

### Docker Hub
Pre-built images available at: `ashikap/fastapi-calculator:latest`

```bash
docker pull ashikap/fastapi-calculator:latest
docker run -p 8000:8000 ashikap/fastapi-calculator:latest
```

## CI/CD Pipeline

### GitHub Actions Workflow

The CI/CD pipeline automatically runs on every push to `main` or `master`:

1. **Unit Tests** (Job 1)
   - Sets up PostgreSQL service
   - Installs Python dependencies
   - Runs pytest with coverage

2. **E2E Tests** (Job 2)
   - Sets up PostgreSQL service
   - Installs Playwright
   - Starts FastAPI server
   - Runs Playwright E2E tests
   - Uploads screenshots on failure

3. **Build & Push** (Job 3)
   - Builds Docker image
   - Pushes to Docker Hub (only on successful tests)

### Required Secrets

Configure these in GitHub Settings → Secrets:
- `DOCKER_USERNAME`: Your Docker Hub username
- `DOCKER_PASSWORD`: Your Docker Hub access token

## Project Structure

```
fast_api_calculator/
├── app/
│   ├── main.py              # FastAPI application
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # JWT authentication
│   ├── database.py          # Database configuration
│   ├── config.py            # Settings
│   └── routers/
│       ├── users.py         # User endpoints
│       └── calculations.py  # Calculation endpoints
├── tests/
│   ├── test_users.py        # User unit tests
│   ├── test_calculations.py # Calculation unit tests
│   ├── test_auth.py         # Auth unit tests
│   └── conftest.py          # Test fixtures
├── e2e/
│   ├── test_auth_e2e.py     # Playwright E2E tests
│   └── conftest.py          # E2E test configuration
├── frontend/
│   ├── register.html        # Registration page
│   ├── login.html           # Login page
│   └── index.html           # Home page
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # GitHub Actions workflow
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## API Endpoints

### Authentication
- `POST /users/register` - Register new user
  ```json
  {
    "username": "string",
    "email": "user@example.com",
    "password": "string"
  }
  ```

- `POST /users/login` - Login and get JWT token
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```

### Calculations (Requires JWT)
- `POST /calculations/` - Create calculation
- `GET /calculations/` - List user's calculations
- `GET /calculations/{id}` - Get specific calculation
- `PUT /calculations/{id}` - Update calculation
- `DELETE /calculations/{id}` - Delete calculation

## Testing Strategy

### Client-Side Validation
- Email format validation using regex
- Password minimum length (8 characters)
- Password confirmation matching
- Real-time error messages

### Server-Side Validation
- Pydantic schema validation
- Duplicate username/email checks
- Password hashing with bcrypt
- JWT token generation and verification

### E2E Test Coverage
- ✅ Valid registration flow
- ✅ Valid login flow
- ✅ Short password rejection
- ✅ Invalid email rejection
- ✅ Password mismatch detection
- ✅ Wrong password handling
- ✅ Nonexistent user handling
- ✅ JWT token storage
- ✅ Page navigation

## Technologies Used

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL/SQLite
- **Authentication**: JWT (python-jose), bcrypt
- **Testing**: pytest, Playwright
- **CI/CD**: GitHub Actions
- **Containerization**: Docker, Docker Compose

## Development

### Adding New Features
1. Create feature branch: `git checkout -b feature/new-feature`
2. Implement changes
3. Write unit tests in `tests/`
4. Write E2E tests in `e2e/` if applicable
5. Run tests locally: `pytest -v`
6. Commit and push
7. Create pull request

### Code Quality
- Follow PEP 8 style guide
- Write docstrings for functions
- Maintain test coverage above 95%
- Run linters: `flake8`, `black`

## Troubleshooting

### Playwright Tests Failing
```bash
# Reinstall browsers
playwright install --force

# Run in headed mode to see what's happening
pytest e2e/ --headed -v
```

### Database Connection Issues
```bash
# Check PostgreSQL is running
pg_isready

# Or use SQLite for local development
export DATABASE_URL=sqlite:///./calculator.db
```

### JWT Token Issues
```bash
# Clear browser localStorage
# In browser console: localStorage.clear()

# Generate new SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License

MIT License - see LICENSE file for details

## Contact

- GitHub: [@ashika2031](https://github.com/ashika2031)
- Repository: [fast_api_calculator](https://github.com/ashika2031/fast_api_calculator)
- Docker Hub: [ashikap/fastapi-calculator](https://hub.docker.com/r/ashikap/fastapi-calculator)

## Acknowledgments

- Module 12: Basic JWT authentication and CRUD operations
- Module 13: Front-end integration and E2E testing
- Module 14: Full BREAD operations on front-end (upcoming)
