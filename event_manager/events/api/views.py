from rest_framework import views
from rest_framework.response import Response
from .serializer import SimpleSerializer


class SimpleView(views.APIView):
    def get(self, request):
        data = {
            "name": "Goofy",
            "age": 99,
        }
        serializer = SimpleSerializer(data)
        return Response(serializer.data)
