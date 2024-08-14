import time, random
from celery import shared_task
from query_api.models import Query


@shared_task()
def send_query(query_id):

    """A task for sending query data to a third-party server 
    and saving the result in the DB """

    time.sleep(random.randint(1,5))

    result = random.choice([True,False])
    print(f"Emulated response is {result}")
    

    # # Emulating a post request to /results endpoint
    # post_request = requests.post(
    #     "http://127.0.0.1:8000/api/result/",
    #     headers={"Content-Type": "application/json"},
    #     data=json.dumps(result_data)  # Convert dict to JSON string
    # )
    # if post_request.status_code != 201:
    #     # Logging the error
    #     print("Failed to save result")
    #     raise APIException(detail="Failed to save result", code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    try:
        query = Query.objects.get(id=query_id)
        query.result = result
        query.save()
        print(f"{query.__str__()} has been updated successfully")
        
    except Exception as e:
        print(e)

        
        
    
    

    
