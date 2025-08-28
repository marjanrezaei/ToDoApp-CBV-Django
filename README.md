ToDoApp-CBV-Django

A sample To-Do application built using Django's Class-Based Views (CBVs) to demonstrate the power and flexibility of CBVs in web development.
GitHub
+2
GitHub
+2

📝 Features

Task Management: Create, read, update, and delete tasks efficiently.

User Authentication: Secure login and registration system.

Class-Based Views: Utilizes Django's CBVs for cleaner and more maintainable code.

Responsive Design: Ensures usability across various devices.

🚀 Installation

Clone the repository:

git clone https://github.com/marjanrezaei/ToDoApp-CBV-Django.git
cd ToDoApp-CBV-Django


Set up a virtual environment:

python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`


Install dependencies:

pip install -r requirements.txt


Apply migrations:

python manage.py migrate


Create a superuser:

python manage.py createsuperuser


Run the development server:

python manage.py runserver


Access the application at http://127.0.0.1:8000
.

📂 Project Structure

The project follows a standard Django structure:

core/: Contains the main application logic.

templates/: HTML templates for rendering views.

static/: CSS, JavaScript, and image files.

media/: User-uploaded files.

docker-compose.yml: Configuration for Docker deployment.

🧪 Testing

To run tests, use:

python manage.py test


📄 License

This project is licensed under the MIT License.

Feel free to modify this template to better fit your project's specifics. If you need further assistance or additional sections, such as deployment instructions or API documentation, don't hesitate to ask!
