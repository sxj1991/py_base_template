from rest_framework import serializers

from apps.login.models import UserModel, DetailModel


class UserSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source="user_id", required=False)
    userName = serializers.CharField(max_length=30, source="user_name")
    detail = serializers.SerializerMethodField()
    createTime = serializers.DateTimeField(source="create_time", required=False)

    def get_detail(self, obj):
        user = obj
        details = DetailModel.objects.filter(user_id=user.user_id)

        ret = []
        for item in details:
            ret.append({"address": item.address, "email": item.email})
        return ret

    def validate(self, attrs):
        name = attrs.get('user_name')
        # 验证参数
        if name == "xxx":
            raise RuntimeError("名字不允许")
        return attrs

    class Meta:
        model = UserModel
        exclude = ['user_name', 'user_id', 'create_time']
