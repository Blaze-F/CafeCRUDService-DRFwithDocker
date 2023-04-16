from django.db import models
from cafe_service.models import BaseModel
from user.models import User


# Create your models here.


class Product(BaseModel):
    name = models.CharField(max_length=20, null=False, db_index=True)
    price = models.IntegerField(null=False)
    cost = models.IntegerField(null=False)
    barcode = models.CharField(max_length=13, null=False)
    expire_date = models.DateTimeField(null=False)
    description = models.CharField(max_length=200)
    size = models.CharField(null=False, max_length=1, default="S")
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")

    class Meta:
        db_table = "cafe_product"
