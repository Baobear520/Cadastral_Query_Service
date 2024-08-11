import time
from random import randint,choice

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from query_api.serializers import QuerySerializer, ResultSerializer


class QueryViewSet(viewsets.ViewSet):
    """
    A views set for posting data to /query endpoint
    """

    def create(self, request):
        data = request.data
        serializer = QuerySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        #emulating a request to a third-party server
        time.sleep(randint(1,5))
        result = choice(['true','false',None]) #true,false or no response

        if result:
            query = serializer.save()
            response_data = {
                "query_id": query.id,
                'result': result
            }
            return Response(data=response_data,status=status.HTTP_201_CREATED)
        else: #imitating a no response from the third-party server
            raise APIException(detail="Server error",code=status.HTTP_500_INTERNAL_SERVER_ERROR)









