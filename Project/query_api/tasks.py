import time, random, logging, requests
from celery import shared_task
from django.db import IntegrityError
from query_api.models import Query

 
logger = logging.getLogger(__name__)


@shared_task()
def send_query(query_id):

    """A task for sending query data to a third-party server 
    and saving the result in the DB """

    try:
        # Emulating a post request to /results endpoint of Third_party_server
        get_request = requests.get(
            "http://localhost:8001/api2/result/"
        )
        print(get_request.status_code)
        result = get_request.json().get('result')
        #if post_request.status_code != 201:
        print(f"Got the result from the 3rd party server - {result}")
        try:
            query = Query.objects.get(id=query_id)
            query.result = result
            query.save()
        
            logger.info(f"{query} has been updated successfully")
        
        except Query.DoesNotExist as e:
            logger.error(e)
    
        except IntegrityError as e:
            logger.error(f"Error updating {query}: {e}")
        except Exception as e:
            logger(e)

    except Exception as e:
        logger.error(e)
        query = Query.objects.get(pk=query_id).delete()
        logger.info(f"Deleted {query.id}")
        

    
    
    

        
        
    
    

    
