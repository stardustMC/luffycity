import logging
from django.db import DatabaseError
from redis import RedisError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger('django')

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    view = context.get('view')
    if response is None:
        if isinstance(exc, DatabaseError):
            logger.error('mysql databse error')
            response = Response({'message': 'mysql databse error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif isinstance(exc, RedisError):
            logger.error('redis数据库异常！[%s] %s' % (view, exc))
            response = Response({'message': '缓存服务器内部错误'}, status=status.HTTP_507_INSUFFICIENT_STORAGE)
        elif isinstance(exc, ZeroDivisionError):
            logger.error('ZeroDivisionError detected')
            response = Response({'message': '0 cannot be divided!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response