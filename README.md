# Flask Habit Tracker App

This is a Flask web application that allows users to track their daily habits. The application is built using the Flask web framework, WTForms for form validation, and SQLAlchemy as the ORM for the database.
Requirements

The following libraries are required to run the application:

    Flask
    WTForms
    SQLAlchemy

To install the dependencies, run the following command:

pip install -r requirements.txt

Configuration

Create a new file named .env in the root directory of the application, and add the following configuration variables:

makefile

SECRET_KEY=your_secret_key
SQLALCHEMY_DATABASE_URI=sqlite:///habits.db

Running the Application

To run the application, navigate to the root directory of the application and run the following command:

arduino

flask run

This will start the development server on http://localhost:5000.
Usage

Once the application is running, navigate to http://localhost:5000 in your web browser to view the home page.

From the home page, you can create a new habit, view your list of habits, edit or delete an existing habit, and mark a habit as completed for the current day.
License

This project is licensed under the MIT License - see the LICENSE file for details.
