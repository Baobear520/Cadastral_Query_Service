from rest_framework.serializers import ModelSerializer
from property_api.models import Property


class PropertySerializer(ModelSerializer):
    """A serializer class for the Property model"""

    class Meta:
        model = Property
        fields = ['cadastral_number','latitude','longitude']