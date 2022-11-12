from rest_framework import serializers

from apps.login.models import UserModel, DetailModel


class UserSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source="user_id", required=False)
    userName = serializers.CharField(max_length=30, source="user_name")
    detail = serializers.SerializerMethodField()

    def get_detail(self, obj):
        user = obj
        details = DetailModel.objects.filter(user_id=user.user_id)

        ret = []
        for item in details:
            ret.append({"address": item.address, "email": item.email})
        return ret

    class Meta:
        model = UserModel
        exclude = ['user_name', 'user_id']
