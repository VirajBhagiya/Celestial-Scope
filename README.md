# 🌌 Celestial Scope
Celestial Scope is a FastAPI-based application that provides authentication and celestial coordinate tracking features. Users can register, log in, and obtain real-time celestial coordinates based on their location.

# ✨ Features

1. 🔒 User Authentication:
- User registration with hashed passwords.
- Login with username and password to obtain JWT tokens.
- Protected endpoints accessible only with valid JWT tokens.

2. 🌟 Celestial Coordinate Tracking:
- Retrieve Right Ascension (RA), Declination (Dec), Altitude, and Azimuth for celestial objects.
- Ephemeris calculations using Skyfield.

# ⚙️ Setup and Configuration

1. Clone the Repository:
``` bash
git clone https://github.com/VirajBhagiya/Celestial-Scope.git
cd Celestial-Scope
```

2. Environment Variables:

- Create a .env file in the root directory and define the following:
``` bash
DATABASE_HOSTNAME=="your-database-hostname"
DATABASE_PORT=="your-database-port"
DATABASE_PASSWORD="your-database-password"
DATABASE_NAME="your-database-name"
DATABASE_USERNAME="your-database-username"
SECRET_KEY="your-secret-key"
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

3. Initialize Database:

- Ensure the database tables are created by running the app. The create_tables function will initialize the database automatically on startup.

4. Run the Server:

- Start the FastAPI server using Uvicorn:
``` bash
cd backend
uvicorn app.main:app --reload
```

The server will be available at `http://127.0.0.1:8000/`.


# 🤝 Contributions
Feel free to fork this repository, make improvements, and submit pull requests. All contributions are welcome!