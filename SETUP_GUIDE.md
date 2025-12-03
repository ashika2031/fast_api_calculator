# Setup and Deployment Guide

## Prerequisites

Before starting, ensure you have:
- Python 3.11 or higher installed
- PostgreSQL installed and running
- Docker and Docker Compose installed (optional, for containerized deployment)
- GitHub account
- Docker Hub account

## Step-by-Step Setup

### 1. Clone and Setup Local Environment

```bash
# Navigate to project directory
cd fast_api_calculator

# Create virtual environment (already done)
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate  # On Windows

# Install dependencies (already done)
pip install -r requirements.txt
```

### 2. Setup PostgreSQL Databases

```bash
# Create main database
createdb calculator_db

# Create test database
createdb test_calculator_db
```

If you don't have PostgreSQL commands in PATH, use psql:

```bash
psql postgres
CREATE DATABASE calculator_db;
CREATE DATABASE test_calculator_db;
\q
```

### 3. Configure Environment Variables

The `.env` file has been created with default values. Update if needed:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/calculator_db
SECRET_KEY=dev-secret-key-please-change-in-production-09876543210
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Important**: Change the SECRET_KEY for production deployment!

### 4. Run the Application Locally

```bash
# Start the FastAPI server
uvicorn app.main:app --reload
```

Visit:
- Application: http://localhost:8000
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 5. Run Tests Locally

```bash
# Run all tests
pytest -v

# Run specific test files
pytest tests/test_users.py -v
pytest tests/test_calculations.py -v

# Run with coverage
pytest --cov=app --cov-report=html
open htmlcov/index.html  # View coverage report
```

### 6. Docker Setup (Alternative)

Instead of local setup, you can use Docker:

```bash
# Build and start containers
docker-compose up --build

# Application will be available at http://localhost:8000

# Stop containers
docker-compose down

# Remove volumes (clean slate)
docker-compose down -v
```

## GitHub Setup and CI/CD

### 1. Initialize Git Repository

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: FastAPI Calculator with auth and CRUD"

# Create GitHub repository (via GitHub website)
# Then add remote and push
git remote add origin https://github.com/YOUR_USERNAME/fast_api_calculator.git
git branch -M main
git push -u origin main
```

### 2. Setup GitHub Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these secrets:

   - **DOCKER_USERNAME**: Your Docker Hub username
   - **DOCKER_PASSWORD**: Your Docker Hub access token (not password!)

#### Creating Docker Hub Access Token:

1. Log in to Docker Hub
2. Click your username → **Account Settings**
3. Click **Security** → **New Access Token**
4. Give it a description (e.g., "GitHub Actions")
5. Copy the token and add it as DOCKER_PASSWORD secret

### 3. Update Docker Hub Username in Workflow

Edit `.github/workflows/ci-cd.yml` and replace `${{ secrets.DOCKER_USERNAME }}` with your actual Docker Hub username in the tags section if needed.

### 4. Push Changes to Trigger CI/CD

```bash
git add .
git commit -m "Configure CI/CD pipeline"
git push origin main
```

### 5. Monitor GitHub Actions

1. Go to your GitHub repository
2. Click the **Actions** tab
3. Watch the workflow execution
4. ✅ Green check = Success
5. ❌ Red X = Failure (click to see logs)

## Manual Testing Guide

### Using Swagger UI (http://localhost:8000/docs)

#### 1. Register a User

1. Expand **POST /users/register**
2. Click **"Try it out"**
3. Enter:
   ```json
   {
     "username": "johndoe",
     "email": "john@example.com",
     "password": "password123"
   }
   ```
4. Click **"Execute"**
5. Should return 201 Created with user data

#### 2. Login

1. Expand **POST /users/login**
2. Click **"Try it out"**
3. Enter:
   ```json
   {
     "username": "johndoe",
     "password": "password123"
   }
   ```
4. Click **"Execute"**
5. Copy the `access_token` from response

#### 3. Authorize

1. Click the **"Authorize"** button (🔒 lock icon at top)
2. Enter: `Bearer YOUR_ACCESS_TOKEN_HERE`
3. Click **"Authorize"**
4. Click **"Close"**

#### 4. Create a Calculation

1. Expand **POST /calculations/**
2. Click **"Try it out"**
3. Enter:
   ```json
   {
     "operation": "add",
     "operand1": 15,
     "operand2": 25
   }
   ```
4. Click **"Execute"**
5. Should return 201 Created with result: 40

#### 5. Browse Calculations

1. Expand **GET /calculations/**
2. Click **"Try it out"**
3. Click **"Execute"**
4. Should return array of all your calculations

#### 6. Read Specific Calculation

1. Copy an `id` from the browse results
2. Expand **GET /calculations/{id}**
3. Click **"Try it out"**
4. Enter the id
5. Click **"Execute"**

#### 7. Edit Calculation

1. Expand **PUT /calculations/{id}**
2. Click **"Try it out"**
3. Enter id and update data:
   ```json
   {
     "operation": "multiply",
     "operand1": 15,
     "operand2": 25
   }
   ```
4. Click **"Execute"**
5. Result should now be 375

#### 8. Delete Calculation

1. Expand **DELETE /calculations/{id}**
2. Click **"Try it out"**
3. Enter the id
4. Click **"Execute"**
5. Should return 204 No Content

## Docker Hub Deployment

After successful CI/CD run:

### Pull and Run Your Image

```bash
# Pull from Docker Hub
docker pull YOUR_DOCKERHUB_USERNAME/fastapi-calculator:latest

# Run the container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://user:password@host.docker.internal:5432/calculator_db \
  -e SECRET_KEY=your-production-secret-key \
  YOUR_DOCKERHUB_USERNAME/fastapi-calculator:latest
```

### Using Docker Compose with Your Image

Create a `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: calculator_db
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    image: YOUR_DOCKERHUB_USERNAME/fastapi-calculator:latest
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://user:password@db:5432/calculator_db
      SECRET_KEY: your-production-secret-key
    depends_on:
      - db

volumes:
  postgres_data:
```

Run with:
```bash
docker-compose -f docker-compose.prod.yml up
```

## Taking Screenshots for Submission

### Screenshot 1: GitHub Actions Workflow Success

1. Go to GitHub repository → **Actions** tab
2. Click on a successful workflow run
3. Take screenshot showing:
   - ✅ Green checkmarks for all jobs
   - Test job completed successfully
   - Build and push job completed successfully
   - Your repository name visible

### Screenshot 2: Application Running in Browser

1. Start application: `uvicorn app.main:app --reload`
2. Open http://localhost:8000/docs
3. Take screenshot showing:
   - Swagger UI interface
   - All endpoints visible (users and calculations)
   - Your browser URL bar showing localhost:8000/docs

### Screenshot 3: Testing User Registration/Login

1. In Swagger UI, execute user registration
2. Take screenshot showing:
   - Request body with user data
   - 201 Created response
   - Response body with user details

### Screenshot 4: Testing Calculation Endpoints

1. After authorization, create a calculation
2. Take screenshot showing:
   - Authorized lock icon (green)
   - Request body with calculation data
   - Response with result
   - 201 Created status

## Troubleshooting

### Database Connection Errors

```bash
# Check if PostgreSQL is running
pg_isready

# Check if databases exist
psql -l | grep calculator

# Recreate databases if needed
dropdb calculator_db
dropdb test_calculator_db
createdb calculator_db
createdb test_calculator_db
```

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Verify installation
pip list | grep fastapi
```

### Docker Issues

```bash
# Clean up everything
docker-compose down -v
docker system prune -a

# Rebuild from scratch
docker-compose up --build --force-recreate
```

### Test Failures

```bash
# Check DATABASE_URL in environment
echo $DATABASE_URL

# Run tests with more verbose output
pytest -vv --tb=long

# Run specific failing test
pytest tests/test_users.py::test_register_user_success -vv
```

### GitHub Actions Failing

1. Check the logs in Actions tab
2. Common issues:
   - Docker Hub credentials not set correctly
   - Wrong secret names (must be DOCKER_USERNAME and DOCKER_PASSWORD)
   - Test database not accessible (should auto-create with postgres service)

## Submission Checklist

- [ ] GitHub repository created and pushed
- [ ] All tests passing locally
- [ ] GitHub Actions workflow running successfully
- [ ] Docker image pushed to Docker Hub
- [ ] README.md complete with instructions
- [ ] Screenshot 1: GitHub Actions success
- [ ] Screenshot 2: Application running in browser
- [ ] Screenshot 3: User registration/login working
- [ ] Screenshot 4: Calculation endpoints working
- [ ] Reflection document written
- [ ] Docker Hub link included in submission

## Next Steps (Module 13)

In the next module, you'll add a front-end to interact with this API. This backend is now complete and ready for integration!

## Support

If you encounter issues:
1. Check the README.md for detailed documentation
2. Review the test files to understand expected behavior
3. Check GitHub Actions logs for CI/CD issues
4. Verify all environment variables are set correctly
5. Ensure PostgreSQL is running and accessible
