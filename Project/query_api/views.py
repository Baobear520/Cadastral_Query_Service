from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import APIException, ValidationError

from query_api.models import Query
from query_api.serializers import QuerySerializer
from query_api.tasks import send_query


class QueryViewSet(viewsets.ViewSet):
    """
    A viewset for the /query endpoint
    """

    def create(self, request):

        try:
            data = request.data
            serializer = QuerySerializer(data=data)
            serializer.is_valid(raise_exception=True)
            
           
            query = serializer.save()
            send_query.delay(query.id)
            

            return Response(
                {"query_id": query.id}, 
                status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"error": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        
        except APIException as e:
            if query.id:
                query.delete()
            return Response(
                {"error": e.detail},status=e.status_code)
        
        except Exception as e:
            print(e)
            if query.id:
                query.delete()
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ResultViewSet(viewsets.ViewSet):
    """A viewset for the /result endpoint"""

    def retrieve(self, request, pk):
        try:
            query = get_object_or_404(Query,pk=pk)
            serializer = QuerySerializer(query)

            return Response(serializer.data,status=status.HTTP_200_OK)
        
        except APIException as e:
            return Response(
                {"error": e.detail},status=e.status_code)
        
        except Exception as e:
            print(e)
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    def partial_update(self, request, pk):
        try:
            query = get_object_or_404(Query,pk=pk)
            result = request.data

            serializer = QuerySerializer(query,data=result,partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data,status=status.HTTP_200_OK)
        
        except APIException as e:
            return Response(
                {"error": e.detail},status=e.status_code)
        
        except Exception as e:
            print(e)
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class HistoryViewSet(viewsets.ViewSet):
    """A viewset for the /history endpoint"""

    
    def list(self,request):
        #Enable filtering by cadastral-number
        cadastral_number = request.query_params.get('cadastral_number')
        queryset = Query.objects.all()

        #Filter the base queryset
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
            return Response(
                {"error": e.detail},status=e.status_code)
        
        except Exception as e:
            print(e)
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

