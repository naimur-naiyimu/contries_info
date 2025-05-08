# contries_info
# Countries Information Project

A Django-based web application for managing and displaying country information.

## Features
- User authentication system
- Admin interface for content management
- Country data management (CRUD operations)
- Secure user sessions

<pre lang="markdown"> ## 📁 Project Structure 
.
├── .gitignore
├── requirements.txt
├── manage.py
├── countries/
│   ├── management/
│   │   └── commands/
│   │       └── fetch_countries.py  # Custom command to fetch and store country data
│   ├── migrations/
│   ├── templates/                  # Optional templates for HTML views
│   ├── __init__.py
│   ├── admin.py                    # Admin interface registration
│   ├── apps.py
│   ├── models.py                   # Country model
│   ├── serializers.py             # DRF serializer
│   ├── urls.py                    # App-level URL configuration
│   └── views.py                   # API and view logic
└── countryinfo/
    ├── __init__.py
    ├── asgi.py
    ├── settings.py                # Project settings
    ├── urls.py                   # Project-level URL routing
    └── wsgi.py

</pre>

## Installation
1. Clone the repository:
```bash
git clone https://github.com/naimur-naiyimu/contries_info.git
```
2. Set Up Virtual Environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```
2.1. SQLite Setup: 
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
3. Install requirements:
```bash
pip install -r requirements.txt
```
4. Running the Application:
```bash
python manage.py runserver
```

# API Endpoints Documentation

## Base URL
```http://127.0.0.1:8000/```

## Authentication

### 1. Get Authentication Token
```http
GET /accounts/token/
```
### 2. Login
```http
POST /accounts/login/
```
username: admin
password: 1234

### 3. Logout
```http
GET /accounts/logout/
```
### 4. Logout
```http
GET /accounts/logout/
```
### 5. List all countries Create new country
```http
GET /api/countries
```
### 5.1. Create new country
```http
POST /api/countries
```
### 5.2. List all countries ( with UI)
```http
GET /web/
```
### 6. Get specific country
```http
GET /api/countries/{cca2}/
```
### 6.1. Full update
```http
PUT /api/countries/{cca2}/
```
### 6.2. Partial update
```http
PATCH /api/countries/{cca2}/
```
### 6.3. Delete country
```http
DELETE /api/countries/{cca2}/
```
### 6.4. Get specific country ( with UI)
```http
GET /web/countries/<str:cca2>/
```
### 7. Search countries
```http
GET /api/countries/search/?q={query}
```
### 8. Search countries by language 
```http
GET /api/countries/by_language/?language={code}
```

### 9. Get regional countries
```http
GET /api/countries/{cca2}/regional/ 
```


