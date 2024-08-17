import logging, requests, os
from celery import shared_task
from django.db import IntegrityError
from query_api.models import Query


logger = logging.getLogger(__name__)
THIRD_PARTY_SERVER_URL = os.getenv('THIRD_PARTY_SERVER_URL', 'http://localhost:8001/api/result/')


@shared_task()
def send_query(query_id, cadastral_number):
    """A task for sending query data to a third-party server 
    and saving the result in the DB """
    
    try:
        # Sending a GET request to the third-party server
        response = requests.get(
            THIRD_PARTY_SERVER_URL,
            params={'cadastral_number': cadastral_number},
            timeout=60
        )
        logger.info(f"Received response from Third_party_server with status {response.status_code}")

        # Handle 404 Not Found response
        if response.status_code == 404:
            logger.info(f"No property found with cadastral_number {cadastral_number}.")
            result = False
        elif response.status_code == 200:
            # Try to extract JSON response and handle it
            try:
                result = response.json().get('result')
                if result is None:
                    raise ValueError("The 'result' key is missing in the response.")
                logger.info(f"Existance of the property with cadastral_number {cadastral_number} - {result}")

            except ValueError as e:
                logger.error(f"Error processing the JSON response: {e}")
                _delete_query(query_id)
                return  # Exit the function after handling this case
        else:
            logger.error(f"Unexpected response status: {response.status_code}")
            _delete_query(query_id)
            return  # Exit the function after handling this case
        
        # Try to update the query result in the database
        try:
            logger.info(f"Trying to update the query {query_id} with result.")
            query = Query.objects.get(pk=query_id)
            query.result = result
            query.save()
            logger.info(f"Query {query.id} has been updated successfully.")
        
        except Query.DoesNotExist as e:
            logger.error(f"Query with id {query_id} does not exist: {e}")
            return
        except IntegrityError as e:
            logger.error(f"Error updating query {query_id}: {e}")
            return
        except Exception as e:
            logger.error(f"Unexpected error while updating query {query_id}: {e}")
            return
    # Handle network errors, timeout errors, and unexpected exceptions
    except requests.RequestException as e:
        logger.error(f"Network-related error occurred while processing query {query_id}: {e}")
        _delete_query(query_id)
        return

    except Exception as e:
        logger.error(f"An unexpected error occurred while processing query {query_id}: {e}")
        _delete_query(query_id)
        return


def _delete_query(query_id):
    """Helper function to delete a query."""
    try:
        query = Query.objects.get(pk=query_id)
        query.delete()
        logger.info(f"Deleted query with id {query.id}.")
    except Query.DoesNotExist:
        logger.error(f"Query with id {query_id} not found during deletion.")
    except Exception as e:
        logger.error(f"Unexpected error while deleting query {query_id}: {e}")


        

    
    
    

        
        
    
    

    
