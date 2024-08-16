import time, random, logging, requests
from celery import shared_task
from django.db import IntegrityError
from query_api.models import Query

 
logger = logging.getLogger(__name__)


@shared_task()
def send_query(query_id,cadastral_number):

    """A task for sending query data to a third-party server 
    and saving the result in the DB """


    try:
        # Sending a get request to /results endpoint of Third_party_server
        response = requests.get(
            "http://localhost:8001/api2/result/",
            params={'cadastral_number': cadastral_number},
            timeout=60
        )
        logger.info(f"Received response from Third_party_server with the status {response.status_code}")
        result = response.json().get('result')
        #if post_request.status_code != 201:
        logger.info(f"Got the result from the Third_party_server - {result}")
        try:
            logger.info(f"Trying to add the result to the query{query_id}")
            query = Query.objects.get(pk=query_id)
            query.result = result
            query.save()
        
            logger.info(f"{query} has been updated successfully")
            logger.info()
        
        except Query.DoesNotExist as e:
            logger.error(e)
    
        except IntegrityError as e:
            logger.error(f"Error updating {query}: {e}")
        except Exception as e:
            logger(e)
    #If get request fails, deleting the query from the DB
    except Exception as e:
        logger.error(e)
        query = Query.objects.get(pk=query_id)
        query.delete()
        logger.info(f"Deleted {query.id}")
        

    
    
    

        
        
    
    

    
