from django.db import models


# Create your models here.

class UserModel(models.Model):
    user_id = models.AutoField(primary_key=True, db_column="user_id")
    user_name = models.CharField(db_column="user_name", max_length=30)
    password = models.CharField(max_length=50)

    class Meta:
        db_table = "tb_user"

    def __str__(self):
        return self.user_id


class DetailModel(models.Model):
    id = models.AutoField(primary_key=True, db_column="id")
    address = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    user_id = models.IntegerField()

    class Meta:
        db_table = "tb_detail"

    def __str__(self):
        return self.id
