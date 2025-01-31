# Django Student Management System

## Overview
The **Django Student Management System** is a web-based application built using **Django 5.1** that helps manage student-related operations efficiently. This system includes features like user authentication, password reset via email, and middleware for enhanced login security.

## Features
- **User Authentication:** Secure login and registration system.
- **Password Reset via Email:** If a user forgets their password, they can enter their email and receive a reset link.
- **Custom Middleware (LoginCheckMiddleware):** A middleware file that enhances login security and validation.
- **Student Management:** Add, update, and delete student records.
- **Role-based Access Control:** Separate views and permissions for admin, teachers, and students.
- **Django Admin Panel Integration:** Manage users and records efficiently from the Django admin panel.
- **Responsive UI:** User-friendly and responsive design for better accessibility.

## Technologies Used
- **Framework:** Django 5.1
- **Database:** SQLite (default) or PostgreSQL (configurable)
- **Frontend:** HTML, CSS, Bootstrap
- **Email Service:** SMTP for sending password reset emails

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/Vignesh21J/Django-Student-Management-System.git
   ```
2. Navigate to the project directory:
   ```sh
   cd Django-Student-Management-System/project
   ```
3. Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
5. Apply migrations:
   ```sh
   python manage.py migrate
   ```
6. Create a superuser:
   ```sh
   python manage.py createsuperuser
   ```
7. Run the server:
   ```sh
   python manage.py runserver
   ```
8. Access the application at:
   ```
   http://127.0.0.1:8000/
   ```

## Usage
- **Admin:** Can add/edit/delete users, students, and manage the system.
- **Teachers:** Can view and manage student records.
- **Students:** Can log in, view their profile, and reset their password if needed.

## Contributing
Feel free to contribute by opening an issue or submitting a pull request.

## License
This project is open-source and available under the MIT License.

## Contact
For any queries, contact **Vignesh21J** via GitHub: [GitHub Profile](https://github.com/Vignesh21J/)

