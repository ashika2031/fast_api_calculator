# FastAPI Calculator Application

A full-featured calculator API built with FastAPI, featuring user authentication, calculation history, complete BREAD operations, advanced calculations (power, modulus, sqrt), reports & statistics, interactive front-end dashboard, and comprehensive E2E testing with Playwright.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/ashika2031/fast_api_calculator.git
cd fast_api_calculator

# Install dependencies
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Install Playwright browsers (for E2E tests)
playwright install chromium

# Run the application
uvicorn app.main:app --reload

# Access the application
# - Calculator Dashboard: http://localhost:8000/static/calculations.html
# - API Documentation: http://localhost:8000/docs
# - Register: http://localhost:8000/static/register.html
```

## ✨ Latest Features

### 📊 Reports & Statistics Feature
- **Usage Analytics Dashboard** - Comprehensive statistics and insights
- **Total Calculations** - Track your calculation history count
- **Operations Breakdown** - Visual breakdown with percentages and progress bars
- **Average Calculations** - See average values of operands used
- **Recent History** - View your last 20 calculations with timestamps
- **Most Used Operation** - Identify your most frequently used operation

### 🔢 Advanced Calculations
- **Power (^)** - Raise numbers to any power: `2^8 = 256`
- **Modulus (%)** - Get remainders: `17 % 5 = 2`
- **Square Root (√)** - Calculate square roots: `√144 = 12`
- All operations include comprehensive error handling and validation

### 🎨 User Experience Improvements
- Profile management page with password change functionality
- Clean navigation (logout only in profile section)
- Color-coded operation badges for all 7 operations
- Real-time calculation results
- Responsive design for all devices

## 🎯 Complete Feature List

## 🎯 Complete Feature List

### Core Features
- **User Authentication**: Secure registration and login with JWT tokens
- **Interactive Dashboard**: Full-featured calculator with BREAD operations
- **Profile Management**: Update username, email, and password
- **Reports & Statistics**: Usage analytics and calculation insights
- **Advanced Operations**: Power, modulus, and square root calculations
- **User Isolation**: Complete data privacy - users only see their own data
- **Real-time Validation**: Client-side and server-side validation

### Calculation Operations (7 Total)
- ➕ **Add**: Addition operations
- ➖ **Subtract**: Subtraction operations
- ✖️ **Multiply**: Multiplication operations
- ➗ **Divide**: Division with zero-prevention
- 🔢 **Power**: Exponential calculations (^)
- 📐 **Modulus**: Remainder operations (%)
- √ **Square Root**: Root calculations

### Pages & UI
- **Registration Page** - User signup with validation
- **Login Page** - Secure authentication
- **Calculator Dashboard** - Main BREAD operations interface
- **Profile Page** - User settings and password management
- **Reports Page** - Statistics and analytics dashboard

## Tech Stack

- **Framework**: FastAPI 0.104.1
- **Database**: SQLite (development) / PostgreSQL (production) with SQLAlchemy ORM
- **Authentication**: JWT with python-jose, bcrypt password hashing
- **Testing**: pytest (unit/integration tests) + Playwright (E2E tests)
- **Front-End**: HTML/CSS/JavaScript with real-time validation
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions with automated testing and deployment
- **API Documentation**: OpenAPI (Swagger UI & ReDoc)

## Project Structure

```
fast_api_calculator/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection and session
│   ├── models.py            # SQLAlchemy models (User, Calculation)
│   ├── schemas.py           # Pydantic schemas for validation
│   ├── auth.py              # JWT authentication utilities
│   └── routers/
│       ├── __init__.py
│       ├── users.py         # User registration, login, profile endpoints
│       └── calculations.py  # Calculation BREAD + statistics endpoints
├── frontend/
│   ├── register.html        # User registration page
│   ├── login.html           # User login page
│   ├── calculations.html    # Calculator dashboard with BREAD operations
│   ├── profile.html         # User profile and settings page
│   └── reports.html         # Statistics and analytics dashboard
├── tests/
│   ├── conftest.py          # Test fixtures and configuration
│   ├── test_main.py         # Main app tests
│   ├── test_users.py        # User endpoint tests (9 tests)
│   ├── test_calculations.py # Calculation CRUD tests (16 tests)
│   ├── test_auth.py         # Authentication tests (5 tests)
│   ├── test_database.py     # Database tests (2 tests)
│   ├── test_profile.py      # Profile management tests (14 tests)
│   ├── test_advanced_calculations.py # Advanced ops tests (22 tests)
│   └── test_reports.py      # Statistics tests (16 tests)
├── e2e/
│   ├── conftest.py          # Playwright test configuration
│   ├── test_auth_e2e.py     # E2E authentication tests
│   ├── test_calculations_e2e.py # E2E BREAD operation tests
│   ├── test_profile_e2e.py  # E2E profile management tests
│   ├── test_advanced_calculations_e2e.py # E2E advanced ops tests
│   └── test_reports_e2e.py  # E2E statistics tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # GitHub Actions CI/CD pipeline
├── Dockerfile               # Docker image configuration
├── docker-compose.yml       # Multi-container setup
├── requirements.txt         # Python dependencies
├── pytest.ini               # Pytest configuration
├── pytest-e2e.ini          # Playwright-specific config
├── .env.example            # Environment variables template
├── REFLECTION.md           # Project reflection and learnings
└── README.md               # This file
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
   - Calculator Dashboard: http://localhost:8000/static/calculations.html
   - Profile Page: http://localhost:8000/static/profile.html
   - Reports & Statistics: http://localhost:8000/static/reports.html

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
    "operation": "add",  // add, subtract, multiply, divide, power, modulus, sqrt
    "operand1": 10,
    "operand2": 5
  }
  ```

- **GET /calculations/**: Browse all calculations (paginated)
- **GET /calculations/stats**: Get usage statistics and analytics
  - Query params: `limit` (default: 10) for recent history count
  - Returns: total calculations, operations breakdown, averages, most used operation, recent history
- **GET /calculations/{id}**: Read a specific calculation
- **PUT /calculations/{id}**: Edit a calculation
- **DELETE /calculations/{id}**: Delete a calculation

### User Profile Endpoints (Require Authentication)

- **GET /users/profile**: Get current user profile
- **PUT /users/profile**: Update username or email
- **PUT /users/profile/password**: Change password

### Supported Operations

- `add`: Addition (10 + 5 = 15)
- `subtract`: Subtraction (10 - 5 = 5)
- `multiply`: Multiplication (10 × 5 = 50)
- `divide`: Division (10 ÷ 5 = 2, prevents division by zero)
- `power`: Exponentiation (2 ^ 8 = 256)
- `modulus`: Remainder (17 % 5 = 2)
- `sqrt`: Square Root (√144 = 12, operand2 ignored)

## Running Tests

### Prerequisites for E2E Tests

Make sure the server is running before executing E2E tests:

```bash
# Terminal 1: Start the server
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Terminal 2: Run E2E tests
pytest e2e/ -v -c pytest-e2e.ini
```

### Run Unit and Integration Tests

```bash
# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run all unit and integration tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=app --cov-report=term-missing

# Run specific test file
pytest tests/test_users.py -v
pytest tests/test_calculations.py -v
pytest tests/test_reports.py -v
pytest tests/test_advanced_calculations.py -v

# Generate HTML coverage report
pytest tests/ --cov=app --cov-report=html
# Open htmlcov/index.html in browser
```

### Run Playwright E2E Tests

```bash
# Make sure Playwright browsers are installed
playwright install chromium

# Start the server first (in another terminal)
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Run all E2E tests
pytest e2e/ -v -c pytest-e2e.ini

# Run specific E2E test files
pytest e2e/test_auth_e2e.py -v -c pytest-e2e.ini
pytest e2e/test_calculations_e2e.py -v -c pytest-e2e.ini
pytest e2e/test_profile_e2e.py -v -c pytest-e2e.ini
pytest e2e/test_reports_e2e.py -v -c pytest-e2e.ini

# Run in headed mode (see browser actions)
pytest e2e/ -v -c pytest-e2e.ini --headed

# Run specific test
pytest e2e/test_reports_e2e.py::TestReportsPageE2E::test_reports_shows_operations_breakdown -v -c pytest-e2e.ini
```

### Run All Tests Together

```bash
# Unit + Integration tests only (recommended for CI)
pytest tests/ -v --cov=app

# Note: E2E tests require a running server, run separately
```

### Test Coverage

**Total: 89 Unit & Integration Tests (100% Passing)**

**Unit & Integration Tests Breakdown**:
- **test_users.py** (9 tests): User registration, login, validation
- **test_auth.py** (5 tests): JWT token generation and validation
- **test_calculations.py** (16 tests): CRUD operations, user isolation
- **test_database.py** (2 tests): Database connection and session
- **test_main.py** (2 tests): Root and health endpoints
- **test_profile.py** (14 tests): Profile updates, password changes
- **test_advanced_calculations.py** (22 tests): Power, modulus, sqrt operations
- **test_reports.py** (16 tests): Statistics, operations breakdown, averages

**E2E Tests** (Created, server-dependent):
- **test_auth_e2e.py**: Authentication flows (registration, login, validation)
- **test_calculations_e2e.py**: Complete BREAD workflows
- **test_profile_e2e.py**: Profile management and password changes
- **test_advanced_calculations_e2e.py**: Advanced operations UI testing
- **test_reports_e2e.py**: Statistics dashboard and data visualization

**Code Coverage**: **100%** (307/307 lines of production code)

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment.

### Pipeline Overview

The CI/CD pipeline automatically:
1. **Runs all unit and integration tests** (89 tests)
2. **Validates code coverage** (100% coverage requirement)
3. **Builds Docker image** with optimized caching
4. **Pushes to Docker Hub** on successful tests
5. **Tags with commit SHA and 'latest'**

### Workflow Configuration

**Trigger**: Push to `main` branch or pull requests

**Jobs**:
1. **Test Job**
   - Sets up Python 3.11 environment
   - Installs dependencies from requirements.txt
   - Runs pytest with coverage (`pytest tests/ --cov=app`)
   - Fails build if tests don't pass or coverage drops

2. **Build and Deploy Job** (runs only after tests pass)
   - Builds Docker image using Dockerfile
   - Authenticates with Docker Hub
   - Pushes image as `ashikap/fastapi-calculator:latest`
   - Also tags with Git commit SHA for versioning

### Setting Up CI/CD in Your Fork

1. **Fork the repository** on GitHub

2. **Add GitHub Secrets**:
   - Navigate to: Repository → Settings → Secrets and variables → Actions
   - Add these secrets:
     - `DOCKER_USERNAME`: Your Docker Hub username
     - `DOCKER_PASSWORD`: Your Docker Hub access token (not password!)
       - Generate token at: https://hub.docker.com/settings/security

3. **Push changes** to trigger workflow:
   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin main
   ```

4. **Monitor execution**:
   - Go to the **Actions** tab in your GitHub repository
   - Watch the workflow run in real-time
   - View test results and build logs

### Pipeline Status

Current pipeline status: [![CI/CD Pipeline](https://github.com/ashika2031/fast_api_calculator/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/ashika2031/fast_api_calculator/actions)

## 🐳 Docker Hub Repository

The Docker image is automatically built and pushed to Docker Hub after all tests pass.

**Docker Hub Repository**: **[ashikap/fastapi-calculator](https://hub.docker.com/r/ashikap/fastapi-calculator)**

### Pulling and Running the Image

**Pull the latest image:**
```bash
docker pull ashikap/fastapi-calculator:latest
```

**Run with Docker:**
```bash
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=sqlite:///./calculator.db \
  -e SECRET_KEY=your-secret-key-change-this \
  -e ALGORITHM=HS256 \
  -e ACCESS_TOKEN_EXPIRE_MINUTES=30 \
  --name fastapi-calculator \
  ashikap/fastapi-calculator:latest
```

**Run with Docker Compose:**
```bash
# Download docker-compose.yml from the repository
docker-compose up -d
```

**Access the application:**
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Frontend: http://localhost:8000/static/register.html

**View logs:**
```bash
docker logs fastapi-calculator
```

**Stop the container:**
```bash
docker stop fastapi-calculator
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

## 📚 Additional Documentation

- **[REFLECTION.md](REFLECTION.md)** - Complete project reflection with insights, challenges, and learnings

## 🔗 Important Links

- **GitHub Repository**: [https://github.com/ashika2031/fast_api_calculator](https://github.com/ashika2031/fast_api_calculator)
- **Docker Hub Image**: [https://hub.docker.com/r/ashikap/fastapi-calculator](https://hub.docker.com/r/ashikap/fastapi-calculator)
- **CI/CD Pipeline**: [https://github.com/ashika2031/fast_api_calculator/actions](https://github.com/ashika2031/fast_api_calculator/actions)
- **Live API Docs**: http://localhost:8000/docs (when running locally)

## 📊 Project Statistics

- **Total Lines of Code**: 3,500+ lines
- **Total Tests**: 89 unit/integration tests (100% passing)
- **Code Coverage**: 100% (307/307 lines)
- **API Endpoints**: 15 endpoints
- **Frontend Pages**: 5 pages (register, login, calculator, profile, reports)
- **Operations Supported**: 7 (add, subtract, multiply, divide, power, modulus, sqrt)
- **Features Implemented**: Authentication, BREAD operations, Advanced calculations, Statistics/Reports, Profile management

## 🎓 Key Learning Outcomes

This project demonstrates comprehensive full-stack development skills:

### Backend Development
- ✅ **FastAPI Framework**: RESTful API design, dependency injection, middleware
- ✅ **Database Management**: SQLAlchemy ORM, database migrations, query optimization
- ✅ **Authentication & Security**: JWT tokens, password hashing (bcrypt), user isolation
- ✅ **Data Validation**: Pydantic schemas, request/response models
- ✅ **Error Handling**: Custom exceptions, validation errors, HTTP status codes

### Frontend Development
- ✅ **Modern HTML/CSS**: Responsive design, gradient backgrounds, animations
- ✅ **JavaScript**: Async/await, fetch API, localStorage, DOM manipulation
- ✅ **Client-Side Validation**: Real-time form validation, error messages
- ✅ **User Experience**: Loading states, success/error feedback, intuitive navigation

### Testing & Quality Assurance
- ✅ **Unit Testing**: pytest fixtures, mocking, isolated tests
- ✅ **Integration Testing**: Database interactions, API endpoint testing
- ✅ **E2E Testing**: Playwright browser automation, user workflow testing
- ✅ **Code Coverage**: 100% coverage achieved and maintained
- ✅ **Test Organization**: Proper test structure, fixtures, configuration

### DevOps & Deployment
- ✅ **Containerization**: Docker multi-stage builds, docker-compose orchestration
- ✅ **CI/CD Pipeline**: GitHub Actions, automated testing, deployment triggers
- ✅ **Version Control**: Git workflows, meaningful commits, branch management
- ✅ **Documentation**: Comprehensive README, API documentation, code comments

### Software Engineering Principles
- ✅ **DRY (Don't Repeat Yourself)**: Reusable functions, fixtures, components
- ✅ **SOLID Principles**: Separation of concerns, dependency injection
- ✅ **Security Best Practices**: Input validation, SQL injection prevention, CORS configuration
- ✅ **Code Organization**: Modular structure, clear naming conventions
- ✅ **Error Handling**: Graceful failures, informative error messages

## 📄 License

This project was created as part of academic coursework.

## 👤 Author

**Ashika Patchigolla**
- GitHub: [@ashika2031](https://github.com/ashika2031)
- Project: FastAPI Calculator with Complete BREAD Operations

---

**Built with ❤️ using FastAPI, Playwright, and modern DevOps practices**

