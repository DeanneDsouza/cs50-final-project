# EVENT PLANNAR
#### Video Demo:  <URL https://www.youtube.com/watch?v=R_AGR77--pI>
#### Description: 
Web Application Overview
This web application is designed to help you manage and prioritize events based on their importance. Events are categorized, with the most critical events displayed at the top and less urgent tasks at the bottom. Once an event is completed, it can easily be removed from the list.

Key Features
    Home Page Layout: The layout is simple and user-friendly, created using HTML and styled to provide easy navigation.
    Key buttons include:
        Add Event: Redirects to a page where you can input a new event.
        Login: Takes you to the login page.
        Logout: Logs you out of the application.
        Change Password: Allows you to update your password.
    This layout serves as the base template for the entire website, implemented using Jinja2 for templating in Flask.


User Authentication:
    Login Page: Existing users can log in with their credentials.
    Registration: If you don’t have an account, you can register. The registration process stores your username and a securely hashed password in the database. After registering, you are automatically redirected to the home page.
    Security: Passwords are securely hashed, ensuring that even if the database is accessed, your password remains safe.


Home Page
This is the main interface of the application, where you can view all your events.
Events are displayed according to their importance:
    Very Important events are at the top.
    Can Be Done Later events are at the bottom.
For each event, details like the event name, date, and status are shown.
Each event has a Completed button, allowing you to delete it once it's done.

Add Event Page
Accessible from the home page, this page lets you input details for a new event.
Fields include:
    Event Name: A text input for the event's title.
    Date: A date picker to schedule the event.
    Importance Level: Radio buttons to set the priority of the event.

Change Password Function
Allows you to update your password securely.
This page is accessible from the home page.

Logout Function
Logs you out of the application securely.
You can log back in anytime using your existing username and password.

Technical Details
    Backend: The application is powered by Flask, a lightweight Python web framework.
    Templating: Jinja2 is used to connect and render HTML templates dynamically.
    Database: User credentials and events are stored in a database, with password hashing to ensure security.
    App Structure: The core logic is contained within the app.py file, where all routes, forms, and functions are defined.

#### TODO: first make an id and password. Then once the home page opens, use the add event button to add events.