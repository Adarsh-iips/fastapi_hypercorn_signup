FastAPI Role-Based Signup/Login System with Hypercorn
This project is a web application built using FastAPI and Hypercorn as the ASGI server. It allows users to sign up and log in as either a Doctor or a Patient, and redirects them to their respective dashboards. It includes form validation, profile picture upload, and secure password hashing.

Features:
1. Secure signup and login for two user roles: Patient and Doctor

2. Form data processing with profile image upload

3. Role-based dashboard redirection after login

4. Passwords stored securely using hashing (bcrypt)

5. Jinja2 templates for rendering dynamic HTML pages

6. High-performance async server using Hypercorn


Technologies Used:
a. FastAPI – Web framework

b. Hypercorn – ASGI server

c. Jinja2 – Templating engine

d. Passlib – Password hashing

e. python-multipart – For file uploads

f. Pydantic – Data validation

g. HTML/CSS – Frontend templating


Launch the Project in Minutes:
1. Install all required packages
Open your terminal and run:
pip install -r requirements.txt

2. Fire up the server using Hypercorn
python -m hypercorn app.main:app --config hypercorn_config.py

3. Jump into action
Open your browser and visit:
http://localhost:8000/signup

