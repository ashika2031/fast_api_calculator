# FastAPI Calculator Project - Reflection

## Module 12 & 13: Complete Full-Stack Authentication with E2E Testing

In Module 12, I completed a full backend for the FastAPI calculator by wiring together user authentication and calculation CRUD routes on top of my existing models. Implementing registration, login, and JWT-based auth forced me to think more carefully about security basics like password hashing, token expiry, and not exposing sensitive fields in responses. Once the auth flow was stable, I connected it to the calculation endpoints so that each user only sees and manages their own calculations.

Working with SQLAlchemy and Pydantic together was a good exercise in separation of concerns. The SQLAlchemy models handle persistence and relationships, while the Pydantic schemas define exactly what the API accepts and returns. I had to adjust my schemas a few times to avoid leaking things like hashed passwords and to make sure IDs and data types were consistent across the app and tests. This helped me appreciate how strong typing and clear schemas reduce bugs at the integration level.

Integration testing with pytest was another big learning outcome. Instead of just hitting endpoints manually in the docs, I wrote tests that spin up the app, use a test database, register a user, obtain a token, and then exercise the calculation routes end-to-end. Getting the test database and fixtures configured correctly took some trial and error, but once it worked I had much more confidence that changes to one part of the system wouldn't silently break others.

Setting up GitHub Actions and Docker Hub tied everything together in a DevOps pipeline. I configured the workflow to run tests on every push and build/push a Docker image when the pipeline passes, using secrets to log in to Docker Hub securely. This automated loop—from writing code, to tests, to a buildable container image—made the project feel like a real service rather than just homework, and it gave me practical experience with the kind of CI/CD setup I'd expect in a production environment.

## Module 13: Front-End Integration and Playwright E2E Testing

Module 13 extended the project significantly by adding front-end HTML pages and comprehensive end-to-end testing with Playwright. Creating the registration and login pages forced me to implement proper client-side validation for email format, password length, and password confirmation matching. This dual-layer validation approach—client-side for immediate user feedback and server-side for security—demonstrated the importance of defense in depth.

Learning Playwright was a steep but rewarding curve. Unlike unit tests that mock interactions, Playwright tests simulate real user behavior in an actual browser. Writing tests that fill forms, click buttons, wait for async operations, and verify success messages gave me confidence that the complete user flow works correctly. The challenge of handling timing issues and async operations taught me to use Playwright's built-in auto-waiting features rather than arbitrary sleep statements.

The most valuable lesson from Module 13 was understanding how E2E tests catch integration issues that unit tests miss. For example, CORS configuration problems and static file serving issues only surfaced when testing through the browser. The Playwright tests found these problems immediately, whereas unit tests all passed. This experience showed me that a comprehensive testing strategy needs multiple layers: unit tests for logic, integration tests for API contracts, and E2E tests for user workflows.

Enhancing the CI/CD pipeline to include Playwright tests made the deployment process more robust. The three-stage pipeline—unit tests, E2E tests, then Docker build/push—ensures that no broken code reaches production. Watching the entire automated flow work end-to-end, from git push to Docker Hub deployment, felt incredibly satisfying and gave me practical experience with modern DevOps practices.

## Key Takeaways

**Technical Skills Developed**:
- JWT authentication implementation with python-jose and bcrypt
- Client-side and server-side validation strategies
- Playwright E2E testing with pytest integration
- Multi-stage CI/CD pipelines with GitHub Actions
- Docker containerization and automated deployment
- SQLAlchemy ORM with proper model relationships
- FastAPI with HTTPBearer security schemes

**Challenges Overcome**:
- Debugging bcrypt version compatibility issues (5.0.0 → 4.0.1)
- Configuring CORS for front-end/back-end communication
- Managing async timing in Playwright tests
- Setting up PostgreSQL service containers in GitHub Actions
- Orchestrating multi-job workflows with dependencies

**Time Investment**: Approximately 25 hours total across both modules
- Module 12: ~9 hours (backend implementation and unit tests)
- Module 13: ~16 hours (front-end pages, Playwright, CI/CD enhancement)

**Project Stats**:
- 47 automated tests (34 unit + 13 E2E)
- 99% code coverage
- 3-stage CI/CD pipeline
- 2,377 new lines of code in Module 13
- 100% functionality requirements met

This project transformed from a simple API into a production-ready application with comprehensive testing, professional front-end, and automated deployment. The skills learned—especially E2E testing and advanced CI/CD—will be directly applicable to professional software development.
