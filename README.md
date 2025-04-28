User Management API
A simple, clean, and modular FastAPI project for user authentication and management, using SQLAlchemy, Pydantic, and following the best practices with a clean folder structure.

🚀 Tech Stack
Python 3.10.12

📂 Project Structure
```
user-management-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── database.py              # Database connection and session
│   ├── create_admin.py          # Script to create admin user
│   ├── models/                  # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── token.py
│   ├── schemas/                 # Pydantic schemas for request and response validation
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── token.py
│   ├── crud/                    # CRUD operations for database interaction
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── token.py
│   ├── routes/                  # API endpoints
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── auth.py
│   └── utils/                   # Utility/helper functions
│       ├── __init__.py
│       ├── security.py
│       └── constants.py
├── requirements.txt             # Project dependencies
├── README.md                     # Project documentation
└── .env                          # Environment variables
```

⚙️ Environment Variables
```
Create a .env file in the project root and add the following:
DB_USER=your_database_username
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=your_database_port
DB_NAME=your_database_name
SECRET_KEY=your_secret_key_for_jwt
```

🛠️ Setup Instructions
1. Clone the repository
git clone https://github.com/faizan-1320/user-management-api.git
cd user-management-api

2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows

3. Install dependencies
pip install -r requirements.txt

4. Run the application
uvicorn app.main:app --reload

5. Access the API docs
Swagger UI: http://localhost:8000/docs
