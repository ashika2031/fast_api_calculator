# 🚀 Quick Reference Card

## One-Line Commands

### Start Everything (Recommended)
```bash
./start.sh
```

### Run Tests Only
```bash
source .venv/bin/activate && pytest -v
```

### Start Server Only
```bash
source .venv/bin/activate && uvicorn app.main:app --reload
```

### Start with Docker
```bash
docker-compose up --build
```

## Important URLs

- **Application**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs
- **API Docs (ReDoc)**: http://localhost:8000/redoc

## Quick Test

### 1. Register a User
```bash
curl -X POST "http://localhost:8000/users/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"test123"}'
```

### 2. Login
```bash
curl -X POST "http://localhost:8000/users/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123"}'
```

### 3. Create Calculation (use token from login)
```bash
curl -X POST "http://localhost:8000/calculations/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"operation":"add","operand1":10,"operand2":5}'
```

## Database Setup

```bash
# Create databases
createdb calculator_db
createdb test_calculator_db

# Or via psql
psql postgres -c "CREATE DATABASE calculator_db;"
psql postgres -c "CREATE DATABASE test_calculator_db;"
```

## Git Commands

```bash
# First time setup
git init
git add .
git commit -m "Initial commit: FastAPI Calculator"
git remote add origin YOUR_REPO_URL
git push -u origin main

# After changes
git add .
git commit -m "Your commit message"
git push
```

## Docker Commands

```bash
# Start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Clean everything
docker-compose down -v
```

## Testing Commands

```bash
# All tests
pytest -v

# Specific file
pytest tests/test_users.py -v

# With coverage
pytest --cov=app --cov-report=html

# Verbose output
pytest -vv --tb=long
```

## Environment Variables

Create `.env` file:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/calculator_db
SECRET_KEY=your-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## GitHub Secrets

Add in Settings → Secrets → Actions:
- `DOCKER_USERNAME` - Your Docker Hub username
- `DOCKER_PASSWORD` - Your Docker Hub access token

## Test Operations

| Operation | Operand1 | Operand2 | Result |
|-----------|----------|----------|--------|
| add | 10 | 5 | 15 |
| subtract | 10 | 5 | 5 |
| multiply | 10 | 5 | 50 |
| divide | 10 | 5 | 2 |

## Common Issues

### "psycopg2 not installed"
```bash
pip install psycopg2-binary
```

### "Database does not exist"
```bash
createdb calculator_db
createdb test_calculator_db
```

### "Permission denied: ./start.sh"
```bash
chmod +x start.sh
```

### "Port 8000 already in use"
```bash
lsof -ti:8000 | xargs kill -9
```

### Tests failing with database error
```bash
dropdb test_calculator_db
createdb test_calculator_db
pytest -v
```

## Project Structure at a Glance

```
fast_api_calculator/
├── app/              ← Your application code
│   ├── main.py      ← Entry point
│   ├── routers/     ← API endpoints
│   │   ├── users.py
│   │   └── calculations.py
│   ├── models.py    ← Database models
│   ├── schemas.py   ← Pydantic schemas
│   └── auth.py      ← JWT authentication
├── tests/           ← Integration tests
├── .github/         ← GitHub Actions
└── docs/            ← Documentation
```

## Submission Checklist

- [ ] Code pushed to GitHub
- [ ] GitHub Actions running successfully
- [ ] Docker Hub configured and image pushed
- [ ] Screenshot: GitHub Actions success
- [ ] Screenshot: App running in browser
- [ ] Screenshot: User registration/login
- [ ] Screenshot: Calculation operations
- [ ] REFLECTION.md filled out
- [ ] GitHub repo URL ready
- [ ] Docker Hub URL ready

## Key Files

| File | Purpose |
|------|---------|
| `README.md` | Full documentation |
| `SETUP_GUIDE.md` | Step-by-step setup |
| `REFLECTION.md` | Learning reflection |
| `PROJECT_SUMMARY.md` | Project overview |
| `QUICK_REFERENCE.md` | This file |
| `start.sh` | Quick start script |

## Need Help?

1. Check `SETUP_GUIDE.md` for detailed instructions
2. Read error messages carefully
3. Review `README.md` troubleshooting section
4. Check GitHub Actions logs
5. Verify environment variables

## Success Indicators

✅ Tests pass: `pytest -v` shows all green
✅ Server starts: No errors when starting uvicorn
✅ Can access docs: http://localhost:8000/docs loads
✅ Can register user: POST /users/register returns 201
✅ Can login: POST /users/login returns token
✅ Can create calculation: POST /calculations/ returns 201

---

**Quick Start**: Just run `./start.sh` and choose option 3!
