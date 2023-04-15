from rest_framework import serializers
from django.core.validators import RegexValidator
from cafe.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


# TODO Barcode DB에 어떻게 때려박는지 알아보기.


class ProducCreateRequestSchema(serializers.Serializer):
    """
    상품 생성 요청에 대한 정의입니다.
    """

    name = serializers.CharField(max_length=20, allow_null=False)
    price = serializers.IntegerField(allow_null=False)
    cost = serializers.IntegerField(allow_null=False)
    barcode = serializers.CharField(
        max_length=13,
        allow_null=False,
        validators=[RegexValidator(regex="^[0-9]{13}$", message="바코드는 13자리 길이의 숫자입니다.")],
    )
    expire_date = serializers.DateTimeField(allow_null=False)
    description = serializers.CharField()
    size = serializers.CharField(max_length=1)


class ProducUpdateRequestSchema(serializers.Serializer):
    """
    상품 업데이트 요청에 대한 정의입니다.
    """

    name = serializers.CharField(max_length=20, allow_null=False)
    price = serializers.IntegerField(allow_null=False)
    cost = serializers.IntegerField(allow_null=False)
    barcode = serializers.CharField(
        max_length=13,
        allow_null=False,
        validators=[RegexValidator(regex="^[0-9]{13}$", message="바코드는 13자리 길이의 숫자입니다.")],
    )
    expire_date = serializers.DateTimeField(allow_null=False)
    description = serializers.CharField()
    size = serializers.CharField(max_length=1)


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "price", "expire_date"]  # TODO 리스트 직렬화 선택 필드 작성


class ProductGetRequestSchema(serializers.Serializer):
    id = serializers.IntegerField()


class ProductSearchRequestSchema(serializers.Serializer):
    search_string = serializers.CharField(max_length=200, allow_null=True)
