import random
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class PropertyView(APIView):

    def get(self, request):
        cadastral_number = request.query_params.get('cadastral_number')
        print(f"Performing a lookup for cadastral_number {cadastral_number}")
        result = random.choice([True,False])

        return Response({"result":result},status=status.HTTP_200_OK)

    

