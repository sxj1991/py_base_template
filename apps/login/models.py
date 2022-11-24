from datetime import datetime

from django.db import models


# Create your models here.

class UserModel(models.Model):
    user_id = models.AutoField(primary_key=True, db_column="user_id")
    user_name = models.CharField(db_column="user_name", max_length=30)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tb_user"

    def __str__(self):
        return self.user_id

    def to_dict(self):
        opts = self._meta
        data = {}
        for f in opts.concrete_fields:
            value = f.value_from_object(self)
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            if f.name == 'user_id':
                data['userId'] = value
                continue
            data[f.name] = value
        return data


class DetailModel(models.Model):
    id = models.AutoField(primary_key=True, db_column="id")
    address = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    user_id = models.IntegerField()

    class Meta:
        db_table = "tb_detail"

    def __str__(self):
        return self.id
