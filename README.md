# REST API for Mobile Contact and Spam Identification App

This project is a REST API designed to be consumed by a mobile app. The app is similar to various popular apps which identify if a number is spam, or allow you to find a person’s name by searching for their phone number.

## Terminology and Assumptions

- Each registered user of the app can have zero or more personal “contacts”.
- The “global database” is the combination of all the registered users and their personal contacts.
- The UI will be built by someone else - you are simply making the REST API endpoints to be consumed by the front end.
- You will be writing the code as if it’s for production use and should thus have the required performance and security. However, only you should use only a web server (the development server is fine) and a database, and just incorporate all concepts using these two servers. Do not use other servers.

## Data to be Stored

For each user, the following data should be stored:

- Name
- Phone Number
- Email Address

## Registration and Profile

- A user has to register with at least name and phone number, along with a password, before using. He can optionally add an email address.
- Only one user can register on the app with a particular phone number.
- A user needs to be logged in to do anything; there is no public access to anything.

## Spam

- A user should be able to mark a number as spam so that other users can identify spammers via the global database.

## Search

- A user can search for a person by name or by phone number in the global database.
- Clicking a search result displays all the details for that person along with the spam likelihood. But the person’s email is only displayed if the person is a registered user and the user who is searching is in the person’s contact list.

## Data Population

- For your testing, you should write a script or other facility that will populate your database with a decent amount of random, sample data.


## Steps to Run the Project

1. **Extract the Project**: Extract the zip file containing the project to a suitable location on your system.
2. **Install Dependencies**: This project requires Python and Django. If not already installed, you can download Python from [here](https://www.python.org/downloads/) and install Django using pip:
    ```
    pip install Django
    ```
    If the project uses other dependencies, they will be listed in a requirements.txt file. You can install these using pip:
    ```
    pip install -r requirements.txt
    ```
3. **Set Up the Database**: This project uses SQLite as its database. Django comes with a built-in database migration system that you can use to initialize the database:
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
4. **Create a Superuser**: If your application has an admin panel, you might want to create a superuser account to access it:
    ```
    python manage.py createsuperuser
    ```
5. **Run the Server**: You can start the Django development server using the following command:
    ```
    python manage.py runserver
    ```
6. **Populate the Database**: You can populate the database using the following command:
    ```
    python manage.py populate_db
    ```

## URLs for Testing Features

- **Register**: This feature allows a new user to register. The URL for this feature is `/register/`.
- **Login**: This feature allows a user to log in. The URL for this feature is `/login/`.
- **Create Contact**: This feature allows a user to create a new contact. The URL for this feature is `/contacts/create`.
- **User Contacts**: This feature allows a user to view all their contacts. The URL for this feature is `/contacts/`.
- **Mark Contact as Spam**: This feature allows a user to mark a specific contact as spam. The URL for this feature is `/contact/<int:contact_id>/spam/`, where `<int:contact_id>` should be replaced with the ID of the contact.
- **Get Spam Numbers**: This feature allows a user to view all spam numbers. The URL for this feature is `/spam_numbers/`.
- **Search by Name**: This feature allows a user to search for contacts by name. The URL for this feature is `/search/name/`.
- **Search by Phone Number**: This feature allows a user to search for contacts by phone number. The URL for this feature is `/search/phone/`.
- **Contact Details**: This feature allows a user to view the details of a specific contact. The URL for this feature is `/contact/<int:contact_id>/`, where `<int:contact_id>` should be replaced with the ID of the contact.
