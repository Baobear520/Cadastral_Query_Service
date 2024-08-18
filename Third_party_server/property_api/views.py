from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Property


class PropertyView(APIView):
    """A view for retrieving a property filtered by cadastral number"""

    def get_object(self, cadastral_number):
        return Property.objects.filter(cadastral_number=cadastral_number).exists()

    def get(self, request):
        cadastral_number = request.query_params.get('cadastral_number')
        
        if not cadastral_number:
            return Response({"error": "Cadastral number is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        property_exists = self.get_object(cadastral_number)
        result = property_exists  # True if exists, False if not
        
        return Response({"result": result}, status=status.HTTP_200_OK)





        



    

