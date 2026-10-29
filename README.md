# Little Lemon Restaurant API — Django REST Framework Capstone

A learning project scaffold for a restaurant website and REST API. It includes Django HTML pages, a menu API, a table-booking API, token-based registration/login/logout endpoints, MySQL configuration, and automated API tests.

## Requirements
- Python 3.12+
- MySQL Server (recommended for the course rubric)
- Dependencies in `requirements.txt`

## Quick start
1. Create a MySQL database:
   ```sql
   CREATE DATABASE littlelemon CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
2. Copy `.env.example` to `.env` and set your local database credentials and a secret key.
3. Install packages: `pip install -r requirements.txt`
4. Apply migrations: `python manage.py migrate`
5. Run tests: `python manage.py test restaurant`
6. Start server: `python manage.py runserver`

For local testing without MySQL, set `DB_ENGINE=sqlite` in `.env`. Use MySQL to demonstrate the MySQL criterion.

## API routes
See `Readme.txt` for peer-review endpoints and Insomnia instructions. Menu and booking APIs are under `/api/`.

## Security
Never commit `.env`, production secrets, or database passwords. Menu creation and modification require authentication. Public booking creation is enabled for the restaurant booking flow; updating or deleting bookings requires authentication.
