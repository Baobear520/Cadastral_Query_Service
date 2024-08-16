import logging, requests
from celery import shared_task
from django.db import IntegrityError
from query_api.models import Query

 
logger = logging.getLogger(__name__)


@shared_task()
def send_query(query_id, cadastral_number):
    """A task for sending query data to a third-party server 
    and saving the result in the DB """

    try:
        # Sending a get request to /results endpoint of Third_party_server running on 8001 port
        response = requests.get(
            "http://localhost:8001/api2/result/",
            params={'cadastral_number': cadastral_number},
            timeout=60
        )
        logger.info(f"Received response from Third_party_server with status {response.status_code}")
        
        # Check if the response is successful and handle accordingly
        if response.status_code == 200:
            result = True 
            logger.info(f"The property with cadastral_number {cadastral_number} exists")
        elif response.status_code == 404:
            result = False
            logger.info(f"The property with cadastral_number {cadastral_number} doesn't exist")
        
        # Try updating the query result in the database
        try:
            logger.info(f"Trying to add the result to the query {query_id}")
            query = Query.objects.get(pk=query_id)
            query.result = result
            query.save()
            logger.info(f"{query} has been updated successfully")
        
        except Query.DoesNotExist as e:
            logger.error(f"Query with id {query_id} does not exist: {e}")
        except IntegrityError as e:
            logger.error(f"Error updating query {query_id}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error while updating query {query_id}: {e}")
    
    # If the get request fails, delete the query from the DB
    except Exception as e:
        logger.error(f"Error occurred while processing query {query_id}: {e}")
        try:
            query = Query.objects.get(pk=query_id)
            query.delete()
            logger.info(f"Deleted query with id {query.id}")

        except Exception as e:
            logger.error(f"Unexpected error while deleting query {query_id}: {e}")

        

    
    
    

        
        
    
    

    
