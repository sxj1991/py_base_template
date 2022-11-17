from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def global_exception_handler(exc, context):
    # 先调用REST framework默认的异常处理方法获得标准错误响应对象
    response = exception_handler(exc, context)

    # 在此处补充自定义的异常处理
    if response is None:
        response = Response({'message': 'error', "details": f"错误信息：{exc}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response
