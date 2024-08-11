from rest_framework.serializers import ModelSerializer

from query_api.models import Query,Results


class QuerySerializer(ModelSerializer):
    """A serializer class for the Query model"""

    class Meta:
        model = Query
        fields = ['id','cadastral_number','latitude','longtitude','created_at','updated_at']
        

class ResultSerializer(ModelSerializer):
    """A serializer class for the Results model"""

    class Meta:
        model = Results
        fields = ['id','query','result','created_at','updated_at']

