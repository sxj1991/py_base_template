from rest_framework import status
from rest_framework.response import Response


class APIResponse(Response):

    def __init__(self, data_status=0, data_msg=None, results=None, http_status=status.HTTP_200_OK, headers=None, exception=False,
                 **kwargs):
        # data的初始状态
        data = {
            'statusCode': data_status,
            'message': data_msg
        }
        # data的响应数据体
        if results is not None:
            data['results'] = results
        # data的其他数据
        data.update(kwargs)
        super().__init__(data=data, status=http_status, headers=headers, exception=exception)
