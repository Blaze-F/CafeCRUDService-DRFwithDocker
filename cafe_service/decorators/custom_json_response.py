from functools import wraps
from exceptions import CustomBaseExecption
from django.http import JsonResponse
from rest_framework import status


# def execption_hanlder():
#     """
#     에러 핸들링용 exception hadler입니다.
#     """
#     def decorator(api_func):
#         @wraps(api_func)
#         def _wrapped_view(request, *args, **kwargs):
#             try:
#                 return api_func(request, *args, **kwargs)
#             except Exception as e:
#                 err_msg = e.msg if isinstance(e, CustomBaseExecption) else e.args[0]
#                 err_status = e.status if hasattr(e, "status") else status.HTTP_400_BAD_REQUEST
#                 return JsonResponse(data={"msg": err_msg}, status=err_status)
#         return _wrapped_view
#     return decorator


def custom_json_response(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            data = func(request, *args, **kwargs)
            code = data["code"]
            msg = data["message"]
            response = data["response_data"]
            response_data = {"meta": {"code": code, "message": msg}, "data": response}
        except Exception as e:
            err_msg = e.msg if isinstance(e, CustomBaseExecption) else e.args[0]
            err_status = e.status if hasattr(e, "status") else status.HTTP_400_BAD_REQUEST
            response_data = {"meta": {"code": err_status, "message": err_msg}, "data": None}
        # Return the response as a JsonResponse
        return JsonResponse(response_data, status=response_data["meta"]["code"])

    return wrapper
