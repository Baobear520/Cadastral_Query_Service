import json
import time, requests
from random import randint,choice
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from query_api.models import Query
from query_api.serializers import QuerySerializer, ResultSerializer


class QueryViewSet(viewsets.ViewSet):
    """
    A views set for posting data to /query endpoint
    """
    def create(self, request):
        data = request.data
        serializer = QuerySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        # Emulate a request to a third-party server
        time.sleep(randint(1, 5))
        result = choice([True, False, None])  # Use boolean values
        
        if result is not None:
            with transaction.atomic():
                query = serializer.save()
                
                result_data = {
                    "query_id": query.id,
                    "result": result
                }
                print(f"Result data to be sent: {result_data}")
                
                # Emulating a post request to /results endpoint
                post_request = requests.post(
                    "http://127.0.0.1:8000/api/result/",
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(result_data)  # Convert dict to JSON string
                )
                if post_request.status_code != 201:
                    # Logging the error
                    print("Failed to save result")
                    raise APIException(detail="Failed to save result", code=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                return Response(data=result_data, status=status.HTTP_201_CREATED)
    
        else: 
            # Imitating a no response from the third-party server
            raise APIException(detail="Server error", code=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ResultViewSet(viewsets.ViewSet):

    def create(self,request):
        query_id = request.data.get('query_id')
        result = request.data.get('result')

        serializer = ResultSerializer(data={
            "query": query_id,
            "result": result
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data,status=status.HTTP_201_CREATED)
    

class HistoryViewSet(viewsets.ViewSet):

    def list(self,request):
        try:
            queryset = Query.objects.all()
            serializer = QuerySerializer(queryset)
            print(serializer.data)
            
            
            return Response(serializer.data,status=status.HTTP_200_OK)

        except Query.DoesNotExist:
            return Response({"error": "No queries found"}, status=status.HTTP_404_NOT_FOUND)
    




