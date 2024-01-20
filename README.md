<div class="badge_container" style="display: flex; justify-content: center;">

![Python Version](https://img.shields.io/badge/python-3.11-blue.svg)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Docker-compose](https://img.shields.io/badge/docker-compose-orange.svg)](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04)
![Linux (Ubuntu)](https://img.shields.io/badge/linux-ubuntu-green.svg)
</div>
<h1 align="center" style="color: #B5E5E8;">Cats for Future API</h1>
The Cats for Future API is designed to facilitate the administration and dynamic content management of an website. It offers a rich set of CRUD operations to efficiently manage and update all data on the site.

Built on the asynchronous FastAPI framework, the API utilizes a PostgreSQL database with the asynchronous adapter asyncpg and Pydantic v2 for data serialization. It features a robust authentication system, employing the JWTStrategy and BearerTransport for secure user authentication and management, powered by the FastAPI-Users and FastAPI-Mail libraries.

<h3 align="center">TECHNOLOGY</h3>
<p align="center">
  <a href="https://fastapi.tiangolo.com/" target="_blank">
    <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="Swagger">
  </a>
  <a href="https://fastapi-users.github.io/fastapi-users" target="_blank">
    <img src="https://img.shields.io/badge/FastAPI%20Users-ef5552?style=for-the-badge" alt="Swagger">
  </a>
  <a href="https://www.sqlalchemy.org/" target="_blank">
    <img src="https://img.shields.io/badge/sqlalchemy-fbfbfb?style=for-the-badge" alt="Swagger">
  </a>
  <a href="https://pydantic-docs.helpmanual.io/" target="_blank">
    <img src="https://img.shields.io/badge/Pydantic-14354C?style=for-the-badge&logo=Pydantic" alt="Swagger">
  </a>
  <a href="https://pypi.org/project/fastapi-mail/" target="_blank">
    <img src="https://img.shields.io/badge/FastAPI%20Mail-0078D4?style=for-the-badge" alt="Swagger">
  </a>
</p>


<h2 align="center" style="color: #B5E5E8;">INSTALLATION</h2>

To run the project, you will need [Docker-compose](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04) installed. Follow these steps to install and run the project:

1. Create a new folder for your project.

2. Open the project in an IDE

3. Initialize Git

    ```
    git init
    ```
4. Add the remote repository
    ```
    git remote add origin https://github.com/baza-trainee/cat_for_future_backend.git
    ```
5. Sync with the remote repository

    ```
    git pull origin dev
    ```
6. Create a `.env` file and define all environment variables from the .`env_example` file:
    <details class="custom-details">
    <summary><b>DB settings</b></summary>
    <p class="custom-details-description"><i>Variables for database and the project configuration.</i></p>

    <b class="variable-name">POSTGRES_HOST</b>=<span class="variable-value">localhost</span><br>
    <b class="variable-name">POSTGRES_PORT</b>=<span class="variable-value">5432</span><br>
    <b class="variable-name">POSTGRES_DB</b>=<span class="variable-value">cats_db</span><br>
    <b class="variable-name">POSTGRES_USER</b>=<span class="variable-value">admin</span><br>
    <b class="variable-name">POSTGRES_PASSWORD</b>=<span class="variable-value">admin</span><br>
    <b class="variable-name">BASE_URL</b>=<span class="variable-value">http://localhost:8000</span><br>
    <b class="variable-name">SECRET_AUTH</b>=<span class="variable-value">SECRET</span>
    </details>

    <details class="custom-details">
    <summary><b>Cloud settings</b></summary>
    <p class="custom-details-description"><i>Variables for configuring Cloudinary cloud service.</i></p>

    <b class="variable-name">CLOUD_NAME</b>=<span class="variable-value">cloudname</span><br>
    <b class="variable-name">API_KEY</b>=<span class="variable-value">1234567890</span><br>
    <b class="variable-name">API_SECRET</b>=<span class="variable-value">1s2e3c4r5e6t</span>
    </details>

    <details class="custom-details">
    <summary><b>Admin settings</b></summary>
    <p class="custom-details-description"><i>Variables for initialization of superuser (administrator).</i></p>

    <b class="variable-name">ADMIN_USERNAME</b>=<span class="variable-value">admin@example.com</span><br>
    <b class="variable-name">ADMIN_PASSWORD</b>=<span class="variable-value">Adm1n123$</span>
    </details>

    <details class="custom-details">
    <summary><b>Mail settings</b></summary>
    <p class="custom-details-description"><i>Variables for configuring FastAPI-Mail service.</i></p>

    <b class="variable-name">EMAIL_HOST</b>=<span class="variable-value">outlook.office365.com or smtp.gmail.com</span><br>
    <b class="variable-name">EMAIL_USER</b>=<span class="variable-value">your email</span><br>
    <b class="variable-name">EMAIL_PASSWORD</b>=<span class="variable-value">Password or Key (if use gmail)</span>
    </details>

<h2 align="center" style="color: #B5E5E8;">USAGE</h2>

1. Create a virtual environment:
    ```
    python -m venv venv
    ```
2. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Run the project using the Makefile command:
    ```
    make run
    ```
    This command will create a container with the database, initiate migrations, and start the server on port `8000`.<br>
    Subsequent launches of the application are carried out with the command:
    ```
    make start
    ```

    <h2 align="center" style="color: #B5E5E8;">DOCUMENTATION</h2>

    Interactive documentation is available at `/docs` and `/redoc` for two different interfaces: [Swagger](https://swagger.io/) and [ReDoc](https://redoc.ly/). They allow you to view and test all the API endpoints, as well as get information about the parameters, data types, and response codes. You can learn more about Swagger and ReDoc on their official websites.
<p align="center">
  <a href="https://swagger.io/" target="_blank">
    <img src="https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=swagger&logoColor=black" alt="Swagger">
  </a>
  <a href="https://redoc.ly/" target="_blank">
    <img src="https://img.shields.io/badge/Redoc-8A2BE2?style=for-the-badge&logo=redoc&logoColor=white" alt="Swagger">
  </a>
</p>
