from django.utils.timezone import now
from rest_framework import mixins,viewsets,status
from rest_framework.response import Response
from query_api.models import Query
from query_api.serializers import QuerySerializer, HistorySerializer
from query_api.tasks import send_query
import logging

logger = logging.getLogger(__name__)

class QueryViewSet(mixins.CreateModelMixin,viewsets.GenericViewSet):
    """
    A viewset for handling Query creation.
    """
    queryset = Query.objects.all()
    serializer_class = QuerySerializer

    def create(self, request, *args, **kwargs):
        
        cadastral_number = request.data.get('cadastral_number')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        query = serializer.save()

        # Start celery task 
        send_query.delay(query.id,cadastral_number)
        logger.info(f"A query with the id={query.id} has been created and added to the database")
        
        return Response(
            {"query_id": query.id}, 
            status=status.HTTP_201_CREATED
        )

class HistoryViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    A viewset for retrieving the history of all queries/a query filtered by a cadastral number.
    """
    serializer_class = HistorySerializer

    def get_queryset(self):
        queryset = Query.objects.all()
        cadastral_number = self.request.query_params.get('cadastral_number')
        if cadastral_number:
            queryset = queryset.filter(cadastral_number=cadastral_number)
        return queryset


class PingViewSet(viewsets.ViewSet):
    """
    A viewset for checking the Query_API server's status.
    """

    def list(self, request):
        return Response({
            "status": "The service is up and running",
            "timestamp": now(),
            "version": "1.0.0"
        }, status=status.HTTP_200_OK)
