Login Web Application

Overview

This project is a web application built with Flask. It provides user authentication, including signup and login functionalities, and allows users to create, store, and delete notes. The application is powered by a SQLite database and is managed through the main.py file.

Features

	•	User Authentication:
	•	Signup: Users can create an account by providing their email, first name, and password.
	•	Login: Registered users can log in to their accounts.
	•	Session Management: Users are remembered across sessions with secure cookies.
	•	Notes Management:
	•	Create Notes: Users can add new notes.
	•	View Notes: Users can view their existing notes.
	•	Delete Notes: Users can delete their notes.

Technologies Used

	•	Backend: Flask
	•	Database: SQLite
	•	ORM: SQLAlchemy
	•	User Authentication: Flask-Login
	•	Password Hashing: Werkzeug Security


Setup and Installation:
`git clone git@github.com:soto2571/python-website.git`

Create a Virtual Environment:
python -m venv venv

Install all dependecies:
pip install -r requirements.txt

Set Up Environment Variables:
Create a .env file in the root directory and add the following:
SECRET_KEY=HOLA

Run the Application:
python main.py

Access the Application:
Open your browser and go to http://127.0.0.1:8080.

Usage

	•	Signup: Navigate to /sign-up to create a new account.
	•	Login: Navigate to /login to log into your account.
	•	Create Note: Once logged in, use the interface to add new notes.
	•	Delete Note: Users can delete their notes from the notes list.

Contributing

Feel free to submit issues or pull requests. Ensure your changes align with the project’s code style and include tests where applicable.