from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from drf_yasg.utils import swagger_auto_schema
from decorators.custom_json_response import custom_json_response


from provider.auth_provider import AuthProvider
from user.repository import UserRepo
from user.service import UserService
from user.serializers import (
    LoginResponseSchema,
    UserLoginSchema,
    UserSignUpSchema,
    UserSignupSerializer,
)

user_repo = UserRepo()
user_service = UserService(user_repo)
auth_provider = AuthProvider()


"""
모든 return은 custom_json_response 데코레이터에서 처리할 수 있게 딕셔너리 형태로 했습니다.
Returns:
    dict : {
        code : status
        message : str
        response_data : any
    }
"""


@swagger_auto_schema(
    method="post",
    request_body=UserLoginSchema,
    operation_description="JWT 토큰이 반환됩니다. 헤더에 넣어주세요",
    responses={200: LoginResponseSchema},
)
@api_view(["POST"])
@custom_json_response()
@parser_classes([JSONParser])
def login(request):
    phone = request.data["phone"]
    password = request.data["password"]
    auth_token = auth_provider.login(phone=phone, password=password)
    return {
        "code": status.HTTP_200_OK,
        "message": "반환된 토큰을 헤더에 넣어주세요.",
        "response_data": auth_token,
    }


# JsonResponse(auth_token, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    method="post",
    request_body=UserSignUpSchema,
    responses={201: UserSignupSerializer},
)
@api_view(["POST"])
@custom_json_response()
@parser_classes([JSONParser])
def signup(request):
    params = request.data
    params = UserSignUpSchema(data=params)
    params.is_valid(raise_exception=True)
    created_user = user_service.create(**params.data)
    return {
        "code": status.HTTP_201_CREATED,
        "message": "회원가입이 완료되었습니다",
        "response_data": created_user,
    }


# JsonResponse(created_user, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method="delete")
@api_view(["DELETE"])
@custom_json_response()
@parser_classes([JSONParser])
def logout(request):
    auth_token = auth_provider.get_token_from_request(request=request)
    auth_provider.logout(auth_token)
    return


# JsonResponse("logouted", status=status.HTTP_202_ACCEPTED)

# {
#         "code":,
#         "message":,
#         "response_data"
#     }

# @api_view(["POST"])
# @execption_hanlder()
# @parser_classes([JSONParser])
# @swagger_auto_schema(
#     responses={"access": "encoded_jwt"},
# )
# def signout(request):
#     auth_token = request.META.get("HTTP_AUTHORIZATION", None)
#     if auth_token != None:
#         auth_token = auth_provider.logout(auth_token)
#     return JsonResponse(auth_token, status=status.HTTP_200_OK)
