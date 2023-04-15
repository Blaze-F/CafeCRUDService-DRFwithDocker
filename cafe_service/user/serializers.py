from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.validators import RegexValidator
from user.models import User as CustomUserModel

User = get_user_model()


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = User.objects.create(
            phone=validated_data["phone"], name=validated_data["name"]
        )  # User 생성
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = "__all__"


class LoginResponseSchema(serializers.Serializer):
    access = serializers.CharField()


class UserSignUpSchema(serializers.Serializer):
    """
    user 회원가입 기능 요청 정의 입니다.
    """

    name = serializers.CharField(max_length=20, allow_null=False)
    phone = serializers.CharField(
        max_length=11,
        allow_null=False,
        validators=[RegexValidator(regex="^010\d{8}$", message="핸드폰 번호는 010으로 시작하는 11자리 숫자입니다")],
    )
    password = serializers.CharField(max_length=255, allow_null=False)


class UserLoginSchema(serializers.Serializer):
    """
    user 로그인 기능 요청 정의 입니다.
    """

    phone = serializers.CharField(
        max_length=11,
        allow_null=False,
        validators=[RegexValidator(regex="^010\d{8}$", message="핸드폰 번호는 010으로 시작하는 11자리 숫자입니다")],
    )
    password = serializers.CharField(max_length=255, allow_null=False)
