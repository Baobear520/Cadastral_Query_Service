import json
import time, requests
from random import randint,choice
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from query_api.models import Query
from query_api.serializers import QuerySerializer
from query_api.tasks import send_query

class QueryViewSet(viewsets.ViewSet):
    """
    A views set for posting data to /query endpoint
    """

    def create(self, request):

        try:
            data = request.data
            serializer = QuerySerializer(data=data)
            serializer.is_valid(raise_exception=True)
            query = serializer.save()
            query_id = query.id

            #Celery task
            #send_query.delay(query_id)

            return Response(
                {"query_id":query_id}, 
                status=status.HTTP_201_CREATED
            )

        except APIException as e:
            query.delete()
            return Response({"error":str(e.detail)})



class ResultViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk):
        try:
            query = get_object_or_404(Query,pk=pk)
            serializer = QuerySerializer(query)

            return Response(serializer.data,status=status.HTTP_200_OK)
        
        except APIException as e:
            print(e)
            return Response({"error":"An unexpected error occured"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def partial_update(self, request, pk):
        try:
            query = get_object_or_404(Query,pk=pk)
            result = request.data

            serializer = QuerySerializer(query,data=result,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data,status=status.HTTP_200_OK)
        except APIException as e:
            print(e)
            return Response({"error":"An unexpected error occured"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HistoryViewSet(viewsets.ViewSet):

    def list(self,request):
        cadastral_number = request.query_params['cadastral_number']
        queryset = Query.objects.all()

        if cadastral_number:
            queryset = queryset.filter(cadastral_number=cadastral_number)
            query = get_object_or_404(queryset)
            serializer = QuerySerializer(query)

            return Response(serializer.data,status=status.HTTP_200_OK)
        
        try:
            serializer = QuerySerializer(queryset,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        except Query.DoesNotExist:
            return Response({"error": "No queries found"}, status=status.HTTP_404_NOT_FOUND)

        except APIException as e:
            print(e)
            return Response({"error":"An unexpected error occured"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



