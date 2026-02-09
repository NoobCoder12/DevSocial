# DevSocialApp

[![Django CI](https://github.com/NoobCoder12/DevSocial/actions/workflows/django-tests.yml/badge.svg)](https://github.com/NoobCoder12/DevSocial/actions/workflows/django-tests.yml)

DevSocialApp is a social media platform designed for developers to share posts, interact with each other through likes and comments, and follow their peers.

## Why this stack?
I wanted to build a full-featured social platform while learning Django's ecosystem end-to-end. Using Django for both backend and frontend allowed me to understand how this framework handles everything from database models to template rendering. I chose Bootstrap 5 for the frontend to focus on backend logic rather than CSS, and SQLite made development fast without the overhead of setting up a separate database server.

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
- **Database**: SQLite (default)
- **Testing**: 
  - **Pytest-Django**: For robust integration testing.
  - **Model Bakery**: For efficient test data generation and relationship handling.

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

### Prerequisites

- Python 3.8 or higher
- `pip` (Python package installer)

### 1. Clone the repository

```bash
git clone https://github.com/NoobCoder12/DevSocial.git
cd DevSocial
```

### 2. Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies

Install the required Python packages using `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file in the root directory based on the `.env.example` file:

```bash
cp .env.example .env
```

Open the `.env` file and set your `DJANGO_SECRET_KEY`. You can generate a secret key using:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Database Migrations

Run the following commands to set up your database:

```bash
python manage.py migrate
```

### 6. Create a Superuser (Optional)

To access the Django admin interface:

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

Start the server using:

```bash
python manage.py runserver
```

The application will be accessible at `http://127.0.0.1:8000/`.

## Future Improvements

Things I'd add if I continue this project:

- Detailed view of other users' profiles
- Notifications about interactions with your post or profile
- Direct messages system
- Hashtag system for post discovery
- API endpoints
- PostgreSQL for production deployment

## License

MIT

---

Feel free to use this as a reference or starting point for your own projects.