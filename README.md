# FastAPI Calculator Application - Module 13

A full-featured calculator API built with FastAPI, featuring user authentication, calculation history, complete CRUD operations, and comprehensive E2E testing with Playwright.

## 🎯 Module 13: JWT Authentication with Client-Side Validation & Playwright E2E

**Latest Updates**:
- ✅ Front-end HTML pages with client-side validation
- ✅ Playwright E2E testing suite (13 tests)
- ✅ Enhanced CI/CD pipeline with automated E2E tests
- ✅ JWT token management in localStorage
- ✅ Automated Docker Hub deployment

## Features

- **User Authentication**: Register and login with JWT tokens
- **Front-End Pages**: Registration and login with client-side validation
- **Calculation Operations**: Add, subtract, multiply, divide
- **BREAD Operations**: Browse, Read, Edit, Add, Delete calculations
- **User Isolation**: Users can only access their own calculations
- **Comprehensive Testing**: 34 unit tests + 13 E2E tests (99% coverage)
- **CI/CD Pipeline**: Automated unit, E2E testing, and Docker deployment
- **OpenAPI Documentation**: Interactive API documentation
- **Playwright E2E Tests**: Automated browser testing for critical user flows

## Tech Stack

- **Framework**: FastAPI 0.104.1
- **Database**: PostgreSQL with SQLAlchemy ORM / SQLite (local dev)
- **Authentication**: JWT with python-jose, bcrypt password hashing
- **Testing**: pytest (unit tests) + Playwright (E2E tests)
- **Front-End**: HTML/CSS/JavaScript with client-side validation
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions (3-stage pipeline: unit → E2E → deploy)

## Project Structure

```
fast_api_calculator/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection and session
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # JWT authentication utilities
│   └── routers/
│       ├── __init__.py
│       ├── users.py         # User registration and login endpoints
│       └── calculations.py  # Calculation CRUD endpoints
├── frontend/
│   ├── register.html        # User registration page
│   ├── login.html           # User login page
│   └── index.html           # Home page
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test fixtures and configuration
│   ├── test_main.py         # Main app tests
│   ├── test_users.py        # User endpoint tests (9 tests)
│   ├── test_calculations.py # Calculation endpoint tests (16 tests)
│   ├── test_auth.py         # Authentication tests (5 tests)
│   └── test_database.py     # Database tests (2 tests)
├── e2e/
│   ├── conftest.py          # Playwright test configuration
│   └── test_auth_e2e.py     # E2E tests for auth flows (13 tests)
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # GitHub Actions workflow (3 jobs)
├── Dockerfile
├── docker-compose.yml
├── MODULE13_README.md       # Module 13 detailed documentation
└── MODULE13_REFLECTION.md   # Development reflection
├── requirements.txt
├── .env.example
└── README.md
```

## Installation & Setup

### Prerequisites

- Python 3.11+
- PostgreSQL
- Docker & Docker Compose (optional)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/ashika2031/fast_api_calculator.git
   cd fast_api_calculator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers (for E2E tests)**
   ```bash
   playwright install chromium
   ```

5. **Set up environment variables**
   ```bash
   # Create .env file
   echo "DATABASE_URL=sqlite:///./calculator.db" > .env
   echo "SECRET_KEY=your-secret-key-here" >> .env
   echo "ALGORITHM=HS256" >> .env
   echo "ACCESS_TOKEN_EXPIRE_MINUTES=30" >> .env
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   **Access the application**:
   - API Documentation: http://localhost:8000/docs
   - Registration Page: http://localhost:8000/static/register.html
   - Login Page: http://localhost:8000/static/login.html
   - Home Page: http://localhost:8000/static/index.html

### Docker Setup

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

   The API will be available at: http://localhost:8000

2. **Stop the containers**
   ```bash
   docker-compose down
   ```

## API Documentation

Once the application is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### User Endpoints

- **POST /users/register**: Register a new user
  ```json
  {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword"
  }
  ```

- **POST /users/login**: Login and receive JWT token
  ```json
  {
    "username": "john_doe",
    "password": "securepassword"
  }
  ```

### Calculation Endpoints (Require Authentication)

- **POST /calculations/**: Create a new calculation
  ```json
  {
    "operation": "add",
    "operand1": 10,
    "operand2": 5
  }
  ```

- **GET /calculations/**: Browse all calculations (paginated)
- **GET /calculations/{id}**: Read a specific calculation
- **PUT /calculations/{id}**: Edit a calculation
- **DELETE /calculations/{id}**: Delete a calculation

### Supported Operations

- `add`: Addition
- `subtract`: Subtraction
- `multiply`: Multiplication
- `divide`: Division (prevents division by zero)

## Running Tests

### Local Testing

### Run Unit Tests

```bash
# Run all unit tests
pytest tests/ -v

# Run specific test file
pytest tests/test_users.py -v
pytest tests/test_calculations.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=term
pytest tests/ --cov=app --cov-report=html  # Generates HTML report in htmlcov/
```

### Run Playwright E2E Tests

```bash
# Make sure server is running first
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Run E2E tests
pytest e2e/ -v --browser chromium

# Run in headed mode (see browser)
pytest e2e/ -v --browser chromium --headed

# Run specific E2E test
pytest e2e/test_auth_e2e.py::TestRegistration::test_register_with_valid_data -v
```

### Run All Tests

```bash
# Unit tests + E2E tests
pytest -v

# With coverage
pytest --cov=app --cov-report=term -v
```

### Test Coverage

The test suite includes:

**Unit Tests (34 tests)**:
- User registration and login tests
- Password validation and hashing tests
- All calculation CRUD operations
- Authentication and authorization tests
- User isolation tests
- Error handling tests

**E2E Tests (13 tests)**:
- Valid registration flow
- Valid login flow
- Short password validation
- Invalid email validation
- Password mismatch detection
- Wrong password handling
- Nonexistent user handling
- Empty field validation
- Page navigation tests

**Total Coverage**: 99% (228/229 lines)

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment.

### Workflow Steps

The CI/CD pipeline consists of 3 jobs:

1. **Unit Test Job**
   - Sets up Python 3.11 environment
   - Spins up PostgreSQL service
   - Installs dependencies
   - Runs pytest unit tests
   - Validates code quality

2. **E2E Test Job** (runs after unit tests pass)
   - Sets up Python and PostgreSQL
   - Installs Playwright and browsers
   - Starts FastAPI server
   - Runs Playwright E2E tests
   - Uploads screenshots on failure

3. **Build and Push Job** (runs after all tests pass)
   - Builds Docker image
   - Logs in to Docker Hub
   - Pushes image as `ashikap/fastapi-calculator:latest`
   - Uses build cache for faster builds

### Setting Up CI/CD

1. **Add GitHub Secrets**
   - Go to your repository → Settings → Secrets and variables → Actions
   - Add the following secrets:
     - `DOCKER_USERNAME`: Your Docker Hub username
     - `DOCKER_PASSWORD`: Your Docker Hub access token

2. **Push to main/master branch**
   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin main
   ```

3. **Monitor the workflow**
   - Go to Actions tab in your GitHub repository
   - Watch the workflow execution

## Docker Hub

The Docker image is automatically pushed to Docker Hub after successful tests.

**Pulling the image:**
```bash
docker pull <your-dockerhub-username>/fastapi-calculator:latest
```

**Running the image:**
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:password@host:5432/calculator_db \
  -e SECRET_KEY=your-secret-key \
  <your-dockerhub-username>/fastapi-calculator:latest
```

## Manual Testing via OpenAPI

1. **Start the application**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Open Swagger UI**: http://localhost:8000/docs

3. **Register a user**
   - Expand POST /users/register
   - Click "Try it out"
   - Enter user details
   - Click "Execute"

4. **Login**
   - Expand POST /users/login
   - Enter credentials
   - Copy the `access_token` from response

5. **Authorize**
   - Click the "Authorize" button (lock icon)
   - Enter: `Bearer <your-access-token>`
   - Click "Authorize"

6. **Test calculation endpoints**
   - Now you can test all calculation endpoints
   - Try creating, reading, updating, and deleting calculations

## Module 13 Documentation

For detailed Module 13 information:

- **📖 [MODULE13_README.md](MODULE13_README.md)** - Comprehensive setup guide, testing instructions, and deployment guide
- **📝 [MODULE13_REFLECTION.md](MODULE13_REFLECTION.md)** - Development reflection, challenges faced, solutions, and learnings
- **📸 [SCREENSHOT_GUIDE.md](SCREENSHOT_GUIDE.md)** - Step-by-step screenshot instructions for submission

## Quick Links

- **GitHub Repository**: https://github.com/ashika2031/fast_api_calculator
- **Docker Hub**: https://hub.docker.com/r/ashikap/fastapi-calculator
- **GitHub Actions**: https://github.com/ashika2031/fast_api_calculator/actions

## Project Statistics

- **Total Tests**: 47 (34 unit + 13 E2E)
- **Test Coverage**: 99% (228/229 lines)
- **Lines of Code**: 2,377+ lines
- **API Endpoints**: 11 endpoints
- **CI/CD Jobs**: 3-stage pipeline
- **Documentation Pages**: 10+ markdown files

