# FastAPI Calculator Application

A full-featured calculator API built with FastAPI, featuring user authentication, calculation history, and complete CRUD operations.

## Features

- **User Authentication**: Register and login with JWT tokens
- **Calculation Operations**: Add, subtract, multiply, divide
- **BREAD Operations**: Browse, Read, Edit, Add, Delete calculations
- **User Isolation**: Users can only access their own calculations
- **Comprehensive Testing**: Integration tests with pytest
- **CI/CD Pipeline**: Automated testing and Docker deployment
- **OpenAPI Documentation**: Interactive API documentation

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT with passlib for password hashing
- **Testing**: pytest with TestClient
- **Containerization**: Docker & Docker Compose
- **CI/CD**: GitHub Actions

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
│   ├── auth.py              # Authentication utilities
│   └── routers/
│       ├── __init__.py
│       ├── users.py         # User registration and login endpoints
│       └── calculations.py  # Calculation CRUD endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test fixtures and configuration
│   ├── test_main.py         # Main app tests
│   ├── test_users.py        # User endpoint tests
│   └── test_calculations.py # Calculation endpoint tests
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # GitHub Actions workflow
├── Dockerfile
├── docker-compose.yml
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
   git clone <your-repo-url>
   cd fast_api_calculator
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and secret key
   ```

5. **Set up PostgreSQL database**
   ```bash
   createdb calculator_db
   createdb test_calculator_db  # For testing
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at: http://localhost:8000

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

1. **Ensure test database exists**
   ```bash
   createdb test_calculator_db
   ```

2. **Run all tests**
   ```bash
   pytest -v
   ```

3. **Run specific test file**
   ```bash
   pytest tests/test_users.py -v
   pytest tests/test_calculations.py -v
   ```

4. **Run with coverage**
   ```bash
   pytest --cov=app --cov-report=html
   ```

### Test Coverage

The test suite includes:
- User registration and login tests
- Password validation and hashing tests
- All calculation CRUD operations
- Authentication and authorization tests
- User isolation tests
- Error handling tests

## CI/CD Pipeline

The project uses GitHub Actions for continuous integration and deployment.

### Workflow Steps

1. **Test Job**
   - Sets up Python environment
   - Spins up PostgreSQL service
   - Installs dependencies
   - Runs pytest suite

2. **Build and Push Job** (on successful test)
   - Builds Docker image
   - Pushes to Docker Hub

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

