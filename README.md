# Book Recommendation Assistant

This is a simple chatbot web application built with **Streamlit** and **MySQL** to help users interact with a book database and receive book recommendations based on SQL queries. The app is integrated with **LangChain** for natural language processing (NLP) and uses **OpenAI's GPT** for generating SQL queries and responses based on user input.

## Features

- **Interactive Chat**: Ask questions about the book database, and the chatbot will respond with SQL-based answers.
- **SQL Query Generation**: Automatically generates SQL queries based on user questions.
- **Polite Responses**: The chatbot responds in a friendly and engaging manner using AI.
- **Database Integration**: The app connects to a MySQL database to fetch book-related information.

## Requirements

Make sure to have the following dependencies installed:

- **Streamlit**: For the web application.
- **LangChain**: For handling SQL queries and interactions with the GPT model.
- **OpenAI**: For generating SQL queries and responses.
- **MySQL**: Database service to store and retrieve book data.
- **Docker**: For running MySQL as a service.

You can install the necessary packages by running:

```bash
pip install -r requirements.txt
```

## Setup Instructions
### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/book-recommendation-assistant.git
cd book-recommendation-assistant
```

### 2. Set Up the Environment
Create a .env file in the root of the project with the following environment variables:

~~~
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=book
MYSQL_ROOT_PASSWORD=your_mysql_root_password
Replace the values with your MySQL user, password, and database settings.
~~~
### 3. Configure Docker
Ensure Docker is installed and running on your machine. The project uses Docker Compose to start the MySQL database.

Run the following command to start the MySQL container:

~~~
docker-compose up -d
~~~
This will start the MySQL container, load the books.sql file to set up the database schema, and expose MySQL on port 3308.

### 4. Run the Streamlit App
Once the database is set up, start the Streamlit app by running:

~~~
streamlit run app.py
~~~
The app will be available in your browser at http://localhost:8501.

### 5. Using the Application
Enter the database connection settings in the sidebar (host, port, user, password, and database name).
Click Connect to connect to the MySQL database.
Start asking questions related to the book database, such as:
~~~
Q: "What are the top 3 most popular books?"
Q: "List 10 books in the database."
~~~
The app will generate SQL queries based on your questions and provide responses in a polite and engaging manner.