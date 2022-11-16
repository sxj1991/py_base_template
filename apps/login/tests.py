from unittest import mock

from django.test import TestCase
import logging

from apps.login.models import UserModel
from apps.org.models import OrgModel

# Create your tests here.
logger = logging.getLogger('only_console_logger')

"""
    django 单元测试
    1. mock数据 模拟model层
    2. 简单的单元测试
"""


class LoginTest(TestCase):

    def setUp(self):
        logger.info(f"初始化测试方法")
        UserModel.objects.get = mock.Mock(
            return_value={"name": "lisi"})

    def test_print_hello(self):
        logger.info(f"执行测试方法")
        user = UserModel.objects.get(user_name="lisi")
        logger.info(f"mock数据:{user['name']}")
        self.assertTrue(user['name'], msg="没有该用户信息")
