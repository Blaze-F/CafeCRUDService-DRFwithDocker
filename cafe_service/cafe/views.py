import json
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from cafe.serializers import (
    ProducCreateRequestSchema,
    ProducUpdateRequestSchema,
    ProductListSerializer,
    ProductSerializer,
)
from drf_yasg import openapi
from cafe.service import CafeService
from cafe.repository import ProductRepository
from decorators.auth_handler import must_be_user
from decorators.custom_json_response import custom_json_response
from provider.auth_provider import AuthProvider
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Parameter, IN_QUERY
from rest_framework import status

repo = ProductRepository()
cafe_service = CafeService(repo=repo)

"""
모든 return은 custom_json_response 데코레이터에서 처리할 수 있게 딕셔너리 형태로 했습니다.
Returns:
    dict : {
        "code" : status,
        "message" : str,
        "response_data" : any,
    }
"""


@swagger_auto_schema(
    method="post",
    request_body=ProducCreateRequestSchema,
    operation_description="새로운 상품이 생성됩니다. 날짜 ",
    responses={201: ProductSerializer},
)
@api_view(["POST"])
@parser_classes([JSONParser])
@custom_json_response()
@must_be_user()
def create_product(request):
    data = cafe_service.create(**request.data, user_id=request.user["id"])
    return_dict: dict = {
        "code": status.HTTP_201_CREATED,
        "message": "상품이 생성되었습니다.",
        "response_data": data,
    }
    return return_dict


@swagger_auto_schema(
    method="put",
    request_body=ProducUpdateRequestSchema,
    operation_description="상품이 업데이트됩니다.",
    responses={202: ProductSerializer},
)
@api_view(["PUT"])
@parser_classes([JSONParser])
@custom_json_response()
@must_be_user()
def update_product(request):
    data = cafe_service.update(**request.data, user_id=request.user["id"])
    return_dict: dict = {
        "code": status.HTTP_202_ACCEPTED,
        "message": "상품이 업데이트됩니다.",
        "response_data": data,
    }
    return return_dict


@swagger_auto_schema(
    method="get",
    operation_description="상품을 단건 조회합니다. 생성자만 가능합니다.",
    responses={200: ProductSerializer},
    manual_parameters=[
        openapi.Parameter(
            "product_id", openapi.IN_QUERY, description="상품 아이디", type=openapi.TYPE_INTEGER
        )
    ],
)
@api_view(["GET"])
@parser_classes([JSONParser])
@custom_json_response()
@must_be_user()
def get_product(request):
    product_id = request.GET["product_id"]
    data = cafe_service.get(product_id=product_id, user_id=request.user["id"])
    return_dict: dict = {
        "code": status.HTTP_200_OK,
        "message": "상품 조회 완료.",
        "response_data": data,
    }
    return return_dict


@swagger_auto_schema(
    method="get",
    operation_description="자신이 업로드한 상품을 다량 조회합니다.",
    responses={200: ProductListSerializer},
    manual_parameters=[
        openapi.Parameter(
            "page", openapi.IN_QUERY, description="페이지 번호", type=openapi.TYPE_INTEGER
        ),
        openapi.Parameter("q", openapi.IN_QUERY, description="검색어", type=openapi.TYPE_STRING),
    ],
)
@api_view(["GET"])
@parser_classes([JSONParser])
@custom_json_response()
@must_be_user()
def find_product_page(request):
    page_num = request.GET["page"]
    search_string = request.GET.get("q")
    data = cafe_service.find(user_id=request.user["id"], page=page_num, search_string=search_string)
    return_dict: dict = {
        "code": status.HTTP_200_OK,
        "message": "상품 조회 완료.",
        "response_data": data,
    }
    return return_dict


@swagger_auto_schema(
    method="delete",
    operation_description="자신의 상품을 삭제합니다",
    manual_parameters=[
        openapi.Parameter(
            "product_id", openapi.IN_QUERY, description="상품 아이디", type=openapi.TYPE_INTEGER
        )
    ],
)
@api_view(["DELETE"])
@parser_classes([JSONParser])
@custom_json_response()
@must_be_user()
def delete_product(request):
    cafe_service.delete(product_id=request.GET["product_id"], user_id=request.user["id"])
    return_dict: dict = {
        "code": status.HTTP_200_OK,
        "message": "상품 삭제 완료.",
        "response_data": None,
    }
    return return_dict
