import logging
from django.db import DatabaseError
from rest_framework.response import Response
from rest_framework.views import exception_handler


logger = logging.getLogger('django')

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        pass
