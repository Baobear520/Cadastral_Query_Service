from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Property
from .serializers import PropertySerializer

class PropertyView(APIView):
    """A view for retrieving a property filtered by cadastral number"""

    def get_object(self, cadastral_number):
        try:
            return Property.objects.get(cadastral_number=cadastral_number)
        except Property.DoesNotExist:
            raise Http404

    def get(self, request):
        cadastral_number = request.query_params.get('cadastral_number')
        if not cadastral_number:
            return Response({"error": "Cadastral number is required"}, status=status.HTTP_400_BAD_REQUEST)

        property_obj = self.get_object(cadastral_number)
        serializer = PropertySerializer(property_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)





        



    

