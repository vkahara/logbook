
# Logbook App

Logbook App is a user-oriented web application that allows users to create, maintain, and share logbooks. It's designed for users who wish to document events, thoughts, or activities and share these with others. The app integrates social features, enabling users to engage with each other's logbooks.
## Features

- **User Authentication**: Secure login and registration functionality to manage user access.
- **Event Management**: Users can create events and associate them with logbooks.
- **Logbook Creation and Sharing**: Users can create logbooks for events, add entries, and share these with others.
- **Interactive UI**: A clean and responsive user interface for an engaging user experience.
- **Social Interactions**: Users can mirror (share) logbooks.

## Installation

Ensure you have Python installed on your system. This app has been tested on Python 3.8+.

1. **Clone the Repository**

   ```sh
   git clone https://github.com/vkahara/logbook.git
   cd logbook/
   ```

2. **Install Dependencies**

   Before running the application, you need to install its dependencies.

   ```sh
   pip install -r requirements.txt
   ```

3. **Database Setup**

   Initialize the database with the required tables.

   ```sh
   python manage.py migrate
   ```

4. **Run the Server**

   Start the application server.

   ```sh
   python manage.py runserver
   ```

   The application will be available at `http://127.0.0.1:8000/`.

## Usage

- **Accessing the Application**: Open your web browser and navigate to `http://127.0.0.1:8000/`.
- **Creating an Account**: Use the "Register" link to create a new user account.
- **Logging In**: Log in with your user credentials to access your dashboard.
- **Creating Events and Logbooks**: Once logged in, you can create new events and associated logbooks, add entries, and share these with other users.
