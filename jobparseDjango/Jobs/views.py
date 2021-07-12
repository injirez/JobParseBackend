from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Jobs
from .serializers import JobsListSerializer
from drf_yasg.utils import swagger_auto_schema

class JobsListView(APIView):

    @swagger_auto_schema(operation_summary="This is all data from Jobs db")
    def get(self, request):
        vacances = Jobs.objects.all()
        serializer = JobsListSerializer(vacances, many=True)

        return Response(serializer.data)
