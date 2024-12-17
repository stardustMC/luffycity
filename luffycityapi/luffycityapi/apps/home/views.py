from rest_framework.views import APIView
from rest_framework.response import Response

import logging
logger = logging.getLogger("django")

# Create your views here.
class TestView(APIView):

    def get(self, request):
        logger.info("GET request received.")
        return Response("Test view returned something.")
