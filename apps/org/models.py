from django.db import models


# 组织模型类
class OrgModel(models.Model):
    org_id = models.AutoField(primary_key=True, db_column="org_id")
    org_name = models.CharField(max_length=50)
    org_type_id = models.ForeignKey('OrgTypeModel', on_delete=models.CASCADE, db_column="org_type_id")

    class Meta:
        db_table = "tb_org"

    def __str__(self):
        return self.org_id


# 组织类型模型类
class OrgTypeModel(models.Model):
    org_type_id = models.AutoField(primary_key=True, db_column="org_type_id")
    org_type = models.CharField(max_length=50)

    class Meta:
        db_table = "tb_org_type"

    def __str__(self):
        return self.org_type_id
