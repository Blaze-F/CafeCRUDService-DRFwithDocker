from rest_framework import serializers
from django_barcode.fields import BarcodeField
from cafe_service.cafe.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


# TODO Barcode DB에 어떻게 때려박는지 알아보기.


class ProducCreateRequestSchema(serializers.Serializer):
    """
    상품 상세정보 요청에 대한 정의입니다.
    """

    name = serializers.CharField(max_length=20, allow_null=False)
    price = serializers.IntegerField(allow_null=False)
    cost = serializers.IntegerField(allow_null=False)
    barcode = BarcodeField()
    expire_date = serializers.DateTimeField(allow_null=False)
    description = serializers.CharField()
    size = serializers.CharField(max_length=1)


class ProducUpdateRequestSchema(serializers.Serializer):
    """
    상품 상세정보 요청에 대한 정의입니다.
    """

    name = serializers.CharField(max_length=20, allow_null=False)
    price = serializers.IntegerField(allow_null=False)
    cost = serializers.IntegerField(allow_null=False)
    barcode = BarcodeField()
    expire_date = serializers.DateTimeField(allow_null=False)
    description = serializers.CharField()
    size = serializers.CharField(max_length=1)


class ProductListSerializer(serializers.ListSerializer):
    class Meta:
        model = Product
        fields = ["name", "price", "expire_date"]  # TODO 리스트 직렬화 선택 필드 작성
