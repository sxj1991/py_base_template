import paramiko

# Create your views here.
from rest_framework import status
from rest_framework.views import APIView

from apps.base_response.api_response import APIResponse


class RemoteViews(APIView):
    def get(self, request):
        # 创建连接类
        client = paramiko.SSHClient()
        # 制定连接远程主机没有本地密钥或HostKeys对象是的策略
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # 连接服务器
        client.connect(hostname='192.168.0.1', port=22, username='root', password='qazwsx123')
        # 建立sftp服务
        sftp = client.open_sftp()
        # 获取目录信息 put上传 get下载
        sftp.listdir("/home/app")
        # 关闭连接
        sftp.close()
        client.close()
        return APIResponse(data_msg="查询成功", http_status=status.HTTP_200_OK)
