
Cadastral Query Service
A Django-based API service for managing and querying cadastral information. This project includes endpoints for querying and managing cadastral data, and integrates with Celery for asynchronous tasks.

Features
Query Management: Create and manage queries.
Result Retrieval: Retrieve results from a third-party server.
Historical Data: Access historical queries and their results.
Asynchronous Tasks: Process tasks asynchronously using Celery.
Installation
Prerequisites
Python 3.8+
Django 4.0+
Celery
A Redis or RabbitMQ broker (for Celery)
Setup
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/cadastral-query-service.git
cd cadastral-query-service
Create and activate a virtual environment:

bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up environment variables:

Create a .env file in the root of the project and add your environment variables:

env
Copy code
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
CELERY_BROKER_URL=redis://localhost:6379/0  # Example for Redis
CELERY_RESULT_BACKEND=redis://localhost:6379/0  # Example for Redis
Run migrations:

bash
Copy code
python manage.py migrate
Create a superuser:

bash
Copy code
python manage.py createsuperuser
Run the development server:

bash
Copy code
python manage.py runserver
The server will be accessible at http://localhost:8000.

Run Celery worker:

In a separate terminal, start the Celery worker:

bash
Copy code
celery -A your_project_name worker --loglevel=info
Usage
API Endpoints
Create a Query

POST /api/query/
Request body: { "cadastral_number": "string", "latitude": float, "longitude": float }
Response: { "query_id": "string" }
Retrieve Results

GET /api/result/
Query parameters: query_id
Response: { "result": "boolean" }
History

GET /api/history/
Response: Paginated list of historical queries.
Testing
Run tests using Django's test runner:

bash
Copy code
python manage.py test
To run specific tests, use:

bash
Copy code
python manage.py test query_api.tests.api_tests


Contact
For any questions or support, please contact your-email@example.com.