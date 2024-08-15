from rest_framework.serializers import ModelSerializer

from query_api.models import Query

class QuerySerializer(ModelSerializer):
    """A serializer class for the Query model"""

    class Meta:
        model = Query
        fields = ['id','cadastral_number','latitude','longtitude']

class HistorySerializer(ModelSerializer):
    """A serializer class for representing Query model at /history endpoint """

    class Meta:
        model = Query
        fields = ['id','cadastral_number','latitude','longtitude','result','created_at','updated_at']
        



