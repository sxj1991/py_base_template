from rest_framework import serializers

from apps.org.models import OrgModel


# 组织类型序列化器
class OrgTypeSerializer(serializers.ModelSerializer):
    orgTypeId = serializers.IntegerField(source="org_type_id", required=False)
    orgType = serializers.CharField(max_length=30, source="org_type")
    org = serializers.SerializerMethodField()

    def get_org(self, obj):
        orgType = obj
        types = OrgModel.objects.filter(org_type_id_id=orgType.org_type_id)
        ret = []
        for item in types:
            ret.append({"orgName": item.org_name})
        return ret

    class Meta:
        model = OrgModel
        exclude = ['org_type_id', 'org_name', 'org_id']
