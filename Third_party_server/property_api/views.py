import random, time
from django.utils.timezone import now
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class PropertyView(APIView):

    def get(self, request):
        time.sleep(random.randint(1,5))

        result = random.choice([True,False])

        return Response({"result":result},status=status.HTTP_200_OK)

    

