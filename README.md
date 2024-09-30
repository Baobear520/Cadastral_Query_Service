---
# Cadastral Query Service

## Task ##
Develop a service for processing real estate queries and sending requests to a third-party server for data validation. The service should store query data, validation results, and the history of all queries in a database. It should include a main API, an admin panel, a caching system, functional tests, documentation, and be deployed using Docker Compose.
## Project Overview
This project is a Django-based service for managing cadastral queries. It integrates several components and technologies, including Celery for asynchronous task processing, Redis as a message broker, Docker Compose for container orchestration, integrated testing and Swagger/OpenAPI for API documentation.

### 1. Integration and Connection of Two Services
The project includes two key services:

- Query_API Service: Handles the core functionality of the application, including creating cadastral queries, and provides the admin interface for managing queries.
- Third-Party Service: A separate Django service running on a different port (e.g., 8001) that stores property data and provides validation of property existence.

Integration:

The main Django service interacts with the third-party service through HTTP requests. For example, it sends GET requests to the /api/result/ endpoint of the third-party service to check property existence based on a cadastral number.

The third-party service responds with JSON data that is used by the main service to update the query results.

### 2. Celery Tasks
Celery is used for handling asynchronous tasks, such as sending queries to the third-party service and updating the database with the results.

### 3. Docker Compose
Docker Compose is used to orchestrate multiple Docker containers for the project.

Configuration: Defined in compose.yml, which includes services for:
MyService: Runs the Query_API Django application.
Third-party-server: Runs the Third_party_server Django application.
Redis: Provides a message broker for Celery
Celery: Handles background tasks.

## Installation
Prerequisites:

- Python 3.8+

- Django 4.0+

- Celery

- Redis

## Setup
Clone the repository:

```
git clone https://github.com/Baobear520/Cadastral-Query-Service.git
```

### First, we must set up the Query_API service located in the Project folder.

```
cd Project
```
Create and activate a virtual environment:

```
python -m venv venv
```

```
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate # On Windows
```

Install dependencies:

```
pip install -r requirements.txt
```

Make migrations to the database:

```
python manage.py makemigrations
```
Run migrations:

```
python manage.py migrate
```
Create a superuser:
```
python manage.py createsuperuser
```

### Next, we need to set up the Third_party_server which is responsible for:
- storing the actual property data;
  
- receiving a GET request to its api/result/ endpoint from Celery and returning a response 

Repeat all the steps the same as for the Query_API.

## Running the project
### In Terminal

Run the Query_API server on port 8000:
```
python manage.py runserver 8000
```
The server will be accessible at http://localhost:8000.

Run Redis:

I ran it from a Docker container bound to http://localhost:6379/0 on my machine

Run Celery worker:

In a separate terminal, start the Celery worker:

```
celery -A config worker --loglevel=info
```
Run the Third_party_server on port 8001:
```
python manage.py runserver 8001
```
The server will be accessible at http://localhost:8001.

### Inside a docker container

To run the Cadastral Query Service in Docker, follow these steps:

#### Prerequisites

- **Docker**: Ensure Docker is installed and running on your machine. You can download it from [Docker's official website](https://www.docker.com/products/docker-desktop).
- **Docker Compose**: Install Docker Compose to manage multi-container Docker applications. It typically comes with Docker Desktop, but you can install it separately from [Docker Compose's official website](https://docs.docker.com/compose/install/).


Create a docker-compose container and run it:
```
docker compose up --build
```
or launch the docker-compose container in the Docker client.

## Usage
### Query_API service
API Endpoints
- Create a Query

POST /api/query/

Request body: { "cadastral_number": "string", "latitude": float, "longitude": float }

Response: { "query_id": "string" }

- Retrieve the history of all queries/a query filtered by a cadastral number.
  
GET /api/history/

Response: Paginated list of historical queries/a query filtered by cadastral_number value

Query parameters: cadastral_number

Response: { "cadastral_number": "string", "latitude": float, "longitude": float, "result": "boolean", "created_at": datetime, "updated_at": datetime }

### Third_party_server
API Endpoints
- Check if a property with a given cadastral number exists

GET /api/result/

Query parameters: cadastral_number

Response: { "result": "boolean" }


## Testing
Run tests using Django's test runner:
```
python manage.py test
```

To run specific tests, use:

```
python manage.py test query_api.tests.test_api
python manage.py test property_api.tests.test_api
```

## Contact
For any questions or support, please contact admitry424@gmail.com
