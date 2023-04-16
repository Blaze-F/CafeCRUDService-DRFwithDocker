import datetime
from cafe.repository import AbstractProductRepo, ProductRepository


from cafe.serializers import ProducCreateRequestSchema
from cafe.serializers import ProducUpdateRequestSchema


class CafeService:
    def __init__(self, repo: AbstractProductRepo) -> None:
        # TODO 나중에 의존성 끊기
        self.repository = ProductRepository()

    def create(
        self,
        name: str,
        price: int,
        cost: int,
        barcode: str,
        expire_date: str,
        description: str,
        size: str,
        user_id: int,
    ) -> dict:
        """
        상품 생성
        view의 scheme에서 params로 입력받습니다.
        Returns:
            dict: 상품 정보
        """
        data = {
            "name": name,
            "price": price,
            "cost": cost,
            "barcode": barcode,
            "expire_date": expire_date,
            "description": description,
            "size": size,
        }
        params = ProducCreateRequestSchema(data=data)
        params.is_valid(raise_exception=True)
        created = self.repository.create(data=params.data, user_id=user_id)
        print(2)
        return created

    def update(
        self,
        product_id: int,
        name: str,
        price: int,
        cost: int,
        barcode: str,
        expire_date: datetime,
        description: str,
        size: str,
        user_id: int,
    ) -> dict:
        """
        상품 업데이트
        view의 scheme에서 **params로 입력받습니다.
        Returns:
            dict: 상품 정보
        """
        data = {
            "product_id": product_id,
            "name": name,
            "price": price,
            "cost": cost,
            "barcode": barcode,
            "expire_date": expire_date,
            "description": description,
            "size": size,
        }
        params = ProducUpdateRequestSchema(data=data)
        params.is_valid(raise_exception=True)
        updated = self.repository.update(product_id=data["product_id"], data=data, user_id=user_id)
        return updated

    def get(self, product_id: int, user_id: int) -> dict:
        """
        Args:
            product_id (int)
        Returns:
            dict: 상품 상세정보
        """
        return_dict = self.repository.get(product_id=product_id, user_id=user_id)
        return return_dict

    def find(self, user_id: int, search_string="", page=1) -> list[dict]:
        """
        검색어를 받아 리스트로 반환합니다.
        Args:
            search_string (str): 검색어(초성 가능)
            pages (int): 페이지 넘버 (1부터 시작)
        Returns:
            list[dict]: 반환되는 리스트 각각의 상품에는 일부 정보만 들어있습니다.
        """
        context, serialized = self.repository.find_page(
            user_id=user_id, search_string=search_string, page=page
        )
        return_list = [context, serialized]
        return return_list

    def delete(self, product_id: int, user_id: int) -> str:
        self.repository.delete(product_id=product_id, user_id=user_id)
        return "success"
