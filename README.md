# End-to-End-UI-Testing-with-Selenium-Project
GA Fifth Project (End-to-End-UI-Testing-with-Selenium-Project) Repository

### Title
End to End UI Testing with Selenium Project

### Description:
This application is used to perform user Sign Up, Login, and operations on transactions, allowing users to send and view transactions. It uses FastAPI. 

### Getting started:
Create a virtual environment:
First, delete the existing venv folder
Then execute the following commands
- python -m venv venv
- venv\Scripts\activate
- pip install -r .\requirements.txt  
To interact with this application, run the app using ```pipenv run uvicorn app.main:app --reload``` and then open your browser to http://127.0.0.1:8000 Then, you will be able to create a new user, log in, send transactions, view the current balance, and view all transactions.
To run the tests, just run ```pytest``` command from another terminal from the main directory of the repository

### Technologies used:
- FastAPI
- Pytest
- HTTPX
- Pydantic
- Selenium

### Route Documentation
| Route | HTTP Method | Description | Parameters |
| -------- | -------- | -------- | -------- |
| /   | GET   | Displays main HTML page | None |
| /signup | POST   | Create new user | None |
| /login | POST   | Authenticate a user and log them in | None |
| /balance | GET   | Get current user’s balance | None |
| /send_transaction | POST   | Add new transaction for the user | None |
| /view_transactions | GET   | View all user's transactions | None |

### Attributions:
This project uses the following libraries:

- [FastAPI](https://fastapi.tiangolo.com/) - A modern, fast (high-performance) web framework for building APIs with Python, based on standard Python type hints. Licensed under the MIT License.
- [Pytest](https://docs.pytest.org/) - A testing framework for writing simple and scalable test cases. Licensed under the MIT License.
- [HTTPX](https://www.python-httpx.org/) - A next-generation HTTP client for Python, supporting HTTP/1.1, HTTP/2, and connection pooling. Licensed under the BSD 3-Clause License.
- [Pydantic](https://docs.pydantic.dev/) - A data validation and settings management library for Python that enforces type hints at runtime and integrates seamlessly with FastAPI. Licensed under the MIT License.
- [Selenium](https://www.selenium.dev/) – A browser automation framework for testing web applications across different browsers and platforms. Licensed under the Apache License 2.0
