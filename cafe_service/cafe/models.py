from django.db import models
from cafe_service.cafe_service.models import BaseModel
from django_barcode.fields import BarcodeField

# Create your models here.


class Product(BaseModel):
    name = models.CharField(max_length=20, null=False)
    price = models.IntegerField(null=False)
    cost = models.IntegerField(null=False)
    barcode = BarcodeField(null=False)
    expire_date = models.DateTimeField(null=False)
    description = models.CharField(max_length=200)
    size = models.CharField(null=False, max_length=1, default="S")
