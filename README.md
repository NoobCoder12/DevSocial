# DevSocialApp

DevSocialApp is a social media platform designed for developers to share posts, interact with each other through likes and comments, and follow their peers.

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
- **Other**: `python-dotenv` for environment variable management, `Pillow` for image handling.

## Project Structure

- `backend/`: Contains the Django project configuration and applications.
  - `apps/`:
    - `users/`: User management, profiles, and authentication.
    - `posts/`: Post creation and feed logic.
    - `interactions/`: Likes, comments, and follow system.
  - `config/`: Project settings and URL routing.
- `frontend/`: Contains static files and HTML templates.
  - `static/`: CSS, JavaScript, and images.
  - `templates/`: Django templates for rendering the UI.
- `manage.py`: Django's command-line utility.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- `pip` (Python package installer)

### 1. Clone the repository

```bash
git clone <repository-url>
cd DevSocialApp
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

Open the `.env` file and set your `DJANGO_SECRET_KEY`.

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

## Critical Fixes Applied

During the preparation of this project, several critical issues were identified and resolved:
- **Model Validation**: Added missing `max_length` to `Comment` model in `interactions` app.
- **Form Logic**: Fixed a bug in `CustomUserCreationForm` where `clean_email` was improperly nested and contained an incorrect database filter.
- **Typo Fixes**: Corrected minor typos in user-facing error messages.
- **Missing Files**: Added `requirements.txt` and `.env.example` to ensure smooth setup.
