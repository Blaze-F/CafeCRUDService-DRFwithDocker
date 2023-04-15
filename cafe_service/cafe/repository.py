import datetime
from cafe.models import Product
from cafe.serializers import ProductListSerializer, ProductSerializer
from config.config import Config
from numpy import ceil
from exceptions import NotFoundError
from user.repository import UserRepo


class AbstractProductRepo:
    def __init__(self) -> None:
        self.model = Product
        self.serializer = ProductSerializer
        self.list_serializer = ProductListSerializer
        self.user_repo = UserRepo()


# TODO Dependency
class ProductRepository(AbstractProductRepo):
    def get(self, product_id: int, user_id: int) -> dict:
        try:
            user_ins = self.user_repo.get_user_ins(user_id=user_id)
            return self.serializer(self.model.objects.get(id=product_id, user=user_ins)).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def get_by_name(self, product_name: str) -> dict:
        try:
            return self.serializer(self.model.objects.get(name=product_name)).data
        except self.model.DoesNotExist:
            raise NotFoundError

    def create(self, data: dict, user_id: int) -> dict:
        """
        Args:
            data (dict):
            user_id (int):
        Returns:
            dict:
        """
        expire_date = self.preprocess_datetme(data["expire_date"])
        user_ins = self.user_repo.get_user_ins(user_id=user_id)
        created = self.model.objects.create(
            user=user_ins,
            name=data["name"],
            price=data["price"],
            cost=data["cost"],
            barcode=data["barcode"],
            expire_date=expire_date,
            description=data["description"],
            size=data["size"],
        )
        return self.serializer(created).data

    def update(self, data: dict, user_id: int, product_id: int) -> dict:
        """
        Update
        Args:
            data (dict)
            user_id (int)
            product_id (int)
        Returns:
            dict:
        """
        user_ins = self.user_repo.get_user_ins(user_id=user_id)
        expire_date = self.preprocess_datetme(data["expire_date"])
        try:
            product_ins = self.model.objects.get(id=product_id, user=user_ins)
            product_ins.name = data["name"]
            product_ins.price = data["price"]
            product_ins.cost = data["cost"]
            product_ins.barcode = data["barcode"]
            product_ins.expire_date = expire_date
            product_ins.description = data["description"]
            product_ins.size = data["size"]
            product_ins.save()
        except self.model.DoesNotExist:
            raise NotFoundError("상품이 존재하지 않습니다.")
        return self.serializer(product_ins).data

    def delete(self, product_id: int, user_id: int) -> None:
        try:
            user_ins = self.user_repo.get_user_ins(user_id=user_id)
            product_instance = self.model.objects.get(id=product_id, user=user_ins)
            product_instance.delete()
        except self.model.DoesNotExist:
            raise NotFoundError("상품이 존재하지 않습니다.")

    def find_page(self, user_id: int, page: int, search_string: str) -> tuple():
        """
        리스트로 반환합니다. 기본 페이지 값은 config에 상수로 두었습니다.
        """
        page_size = Config.page_size["page_size"]
        page_limit = page_size * int(page)
        offset = page_limit - page_size
        try:
            products = self.model.objects.prefetch_related("productdata_set").get(id=user_id)
            data_cnt = products.productdata_set.count()
            pagination = products.productdata_set.all().order_by("sequence")[offset:page_limit]
            serialized = self.serializer(instance=pagination, many=True).data
            page_count = ceil(data_cnt / page_size)
            context = [{"page": page, "page_count": page_count}]
            return context, serialized
        except self.model.DoesNotExist:
            raise NotFoundError("상품이 존재하지 않습니다.")

    def preprocess_datetme(self, timestring: str) -> datetime:
        return datetime.datetime.strptime(timestring, "%Y-%m-%d-%H-%M")
