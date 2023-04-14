import datetime
from cafe_service.cafe.models import Product
from cafe_service.cafe.serializers import ProductSerializer
from exceptions import NotFoundError
from django_barcode.fields import BarcodeField


class AbstractProductRepo:
    def __init__(self) -> None:
        self.model = Product
        self.serializer = ProductSerializer


class ProductRepository(AbstractProductRepo):
    def get(self, product_id: int) -> dict:
        try:
            return self.serializer(self.model.objects.get(id=product_id))
        except self.model.DoesNotExist:
            raise NotFoundError

    def get_by_name(self, product_name: str) -> dict:
        try:
            return self.serializer(self.model.objects.get(name=product_name))
        except self.model.DoesNotExist:
            raise NotFoundError

    def create(
        self,
        name: str,
        price: int,
        cost: int,
        barcode: BarcodeField,
        exprire_date: datetime,
        description: str,
        size: str,
    ):
        serializer = self.serializer(
            data={
                "name": name,
                "price": price,
                "cost": cost,
                "barcode": barcode,
                "exprie_date": exprire_date,
                "description": description,
                "size": size,
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def update(
        self,
        name: str,
        price: int,
        cost: int,
        barcode: BarcodeField,
        exprie_date: datetime,
        description: str,
        size: str,
    ) -> dict:
        serializer = self.serializer(
            data={
                "name": name,
                "price": price,
                "cost": cost,
                "barcode": barcode,
                "exprie_date": exprie_date,
                "description": description,
                "size": size,
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.update()
        return serializer.data

    def delete(self, product_id: int) -> None:
        try:
            product_instance = self.model.objects.get(id=product_id)
            product_instance.delete()
        except self.model.DoesNotExist:
            raise NotFoundError
