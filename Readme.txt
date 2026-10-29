LITTLE LEMON RESTAURANT API - PEER REVIEW GUIDE

Project title: Little Lemon Restaurant API - Django REST Framework Capstone Project

SETUP
1. Install Python 3.12 and MySQL Server.
2. Create a database:
   CREATE DATABASE littlelemon CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
3. Copy .env.example to .env and enter your local MySQL credentials.
4. Install dependencies: pip install -r requirements.txt
5. Run migrations: python manage.py migrate
6. Create an admin account (optional): python manage.py createsuperuser
7. Start server: python manage.py runserver
8. Browse to http://127.0.0.1:8000/ or http://127.0.0.1:8000/api/.

MENU API (GET is public; write operations require authentication)
GET     /api/menu/
POST    /api/menu/
GET     /api/menu/{id}/
PUT     /api/menu/{id}/
PATCH   /api/menu/{id}/
DELETE  /api/menu/{id}/

TABLE BOOKING API (GET and POST are public; PUT/PATCH/DELETE require authentication)
GET     /api/booking/tables/
POST    /api/booking/tables/
GET     /api/booking/tables/{id}/
PUT     /api/booking/tables/{id}/
PATCH   /api/booking/tables/{id}/
DELETE  /api/booking/tables/{id}/
Optional date filter: GET /api/booking/tables/?date=YYYY-MM-DD

AUTHENTICATION
POST    /api/auth/register/   JSON: {"username":"reviewer","email":"reviewer@example.com","password":"StrongPass123!"}
POST    /api/auth/token/      JSON: {"username":"reviewer","password":"StrongPass123!"}
POST    /api/auth/logout/     Requires header: Authorization: Token <token>
For authenticated requests, set the Insomnia header Authorization: Token <token>.

HTML PAGES
GET     /
GET     /book/
GET     /reservations/
Legacy booking JSON endpoint: GET /bookings (optional ?date=YYYY-MM-DD)

TESTS
Run: python manage.py test restaurant

NOTES
- API endpoints are implemented with Django REST Framework.
- MySQL is the default database engine. To run locally without MySQL only, set DB_ENGINE=sqlite in .env; use MySQL when validating the course's database criterion.
- Do not commit .env or real credentials to GitHub.
- Run the test suite and manually verify the API in Insomnia before submitting. Results depend on your local environment.
