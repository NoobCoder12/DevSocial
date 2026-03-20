# DevSocialApp

[![Django CI](https://github.com/NoobCoder12/DevSocial/actions/workflows/django-tests.yml/badge.svg)](https://github.com/NoobCoder12/DevSocial/actions/workflows/django-tests.yml)

> Version 1.1.0

DevSocialApp is a social media platform designed for developers to share posts, interact with each other through likes and comments, and follow their peers.

## Why this stack?
I wanted to build a full-featured social platform while learning Django's ecosystem end-to-end. Using Django for both backend and frontend allowed me to understand how this framework handles everything from database models to template rendering. I chose Bootstrap 5 for the frontend to focus on backend logic rather than CSS, and PostgreSQL was chosen for its reliability and production-readiness, with Docker handling the setup overhead.

The project taught me:
- How Django's ORM handles complex relationships (users, posts, comments, follows)
- Managing user authentication and permissions in Django
- Working with Django's template system and how it differs from separate frontend frameworks
- Structuring a Django project with multiple apps for separation of concerns
- Handling image uploads and media files with Pillow
- The importance of proper form validation and model constraints

## Features

- **User Authentication**: Secure login and user registration.
- **User Profiles**: Customizable profiles with bios and profile pictures.
- **Post Management**: Create and view posts from people you follow.
- **Interactions**:
  - Like and unlike posts.
  - Comment on posts.
  - Follow and unfollow other users.
- **Search**: Search for other developers on the platform.

## Technology Stack

- **Backend**: Django (Python)
- **Frontend**: Django Templates, Bootstrap 5
- **Database**: PostgreSQL
- **Testing**: 
  - **Pytest-Django**: For robust integration testing.
  - **Model Bakery**: For efficient test data generation and relationship handling.
- **DevOps**: Docker    

## Project Structure
```
.
├── .github/workflows
│   └── django-tests.yml     # Config file for GitHub Actions
│    
├── backend/
│   ├── apps/
│   │   ├── interactions/    # Likes, comments, and follow system
│   │   ├── posts/           # Post creation and feed logic
│   │   ├── users/           # User management, profiles, and authentication
│   │   └── conftest.py      # Config file for fixtures
│   │
│   └── config/
│       ├── settings.py      # Django settings
│       ├── urls.py          # URL routing
│       └── wsgi.py          # WSGI configuration
│
├── frontend/
│   ├── static/
│   │   ├── css/             # Stylesheets
│   │   ├── images/          # Static images
│   │   ├── js/              # JavaScript files
│   │   ├── posts/           # Post-related static files
│   │   └── users/           # User-related static files
│   └── templates/
│       ├── layouts/         # Base templates
│       ├── partials/        # Reusable template components
│       ├── posts/           # Post-related templates
│       └── users/           # User-related templates
│
├── pytest.ini               # Pytest configuration file
├── manage.py                # Django's command-line utility
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── init.sql
└── README.md
```

## Testing & Quality Assurance

To ensure the reliability of the social interactions and data integrity, the project includes an automated test suite:

- **Integration Tests**: Built with `Pytest`, covering core logic like user creation, post publishing, and interactions.
- **Data Factories**: Uses `Model Bakery` to handle complex relationships.
- **Data Integrity**: Includes tests for database-level constraints, such as:
    - **Uniqueness**: Preventing duplicate likes/follows.
    - **Business Logic**: Using `CheckConstraints` to prevent users from following themselves.
- **CI/CD Pipeline**: Fully automated testing via **GitHub Actions**. Every `push` and `pull request` triggers the test suite, including database migrations and coverage reporting.

To run tests locally with coverage:

  ```
  pytest --cov=backend/apps --cov-report=term-missing
  ```

All test files are located in app's folders.

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/NoobCoder12/DevSocial.git
cd DevSocial
```

### 2. Create `.env` based on `.env.example`

```bash
DJANGO_SECRET_KEY=your-secret-key-here
POSTGRES_USER=name
POSTGRES_PASSWORD=password
POSTGRES_DB=database-name
POSTGRES_HOST=localhost
```


### 3. Run Docker

```bash
docker compose up
```

The application will be accessible at `http://127.0.0.1:8000/`.

## Future Improvements

Things I'd add if I continue this project:

- Detailed view of other users' profiles
- Notifications about interactions with your post or profile
- Direct messages system
- Hashtag system for post discovery
- API endpoints

## Changelog

### v1.1.0
- Environment created in Docker
- Base changed to PostgreSQL

## License

MIT

---

Feel free to use this as a reference or starting point for your own projects.