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
