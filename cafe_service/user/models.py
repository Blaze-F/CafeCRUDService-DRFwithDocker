from django.db import models

from cafe_service.cafe_service.models import BaseModel


class User(BaseModel):
    password = models.CharField(max_length=255, null=False)
    phone = models.CharField(max_length=13, null=False)
    name = models.CharField(max_length=20, null=False)

    class Meta:
        db_table = "user"
