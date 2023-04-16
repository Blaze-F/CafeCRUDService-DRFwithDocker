# CafeManagementService

</br>

## 목차

  * [개발 기간](#개발-기간)
  * [프로젝트 개요](#프로젝트-개요)
      - [🧹 사용 기술](#-사용-기술)
      - [📰 모델링](#-모델링)
      - [🛠 API Test](#-api-test)
  * [프로젝트 분석](#프로젝트-분석)
  * [실행방법-&-한번-확인해주세요!](#실행방법--한번-확인해주세요)
      - [Config](#config)
  * [API ENDPOINT](#api-endpoint)
      - [user](#user)
      - [product](#product)
  * [🛠 개발 조건](#-개발-조건)
      - [custom_json_response()](#custom_json_response)
      - [logout](#logout)
      - [초성검색](#초성검색)
      - [검증](#검증)
  * [프로젝트 후기](#프로젝트-후기)


## 프로젝트 개요
#### 💭 프로젝트 설명



#### 🧹 사용 기술 

- **Back-End** : Python, Django, Django REST Framework
- **Database** : Mysql
- **deploy** : docker, docker-compose

</br>

#### 개발 기간
## - 2023-04-13 ~ 2023-04-16


#### 📰 모델링
![2023-04-16 23 07 05](https://user-images.githubusercontent.com/101803254/232318778-37af0ce9-e0a7-4c2c-8a27-9b886161d862.png)

database.sql 파일로 남겨두었습니다.
</br>

#### 🛠 API Test

- 2023-04-16 현재 repo 단 테스트 완료되었습니다.

![image](https://user-images.githubusercontent.com/101803254/232319093-18f01685-3886-4b40-8f8a-a8109b252122.png)

확인방법:
```
cd cafe_service
pytest --cov
```

</br>

## 프로젝트 분석
![제목 없는 다이어그램](https://user-images.githubusercontent.com/101803254/202605476-ae90f7da-6548-4582-b99b-4dbdb975fdb3.jpg)

- DB와 직결되는 모델이 실제 비즈니스 레이어, View 까지 넘어가지 않고 중간에 직렬화를 한번 거치게 함으로써 DB와 모델의 무결성을 보장하였습니다.
- 기존 MVC 패턴에서 너무 한쪽이 비대하지고 책임이 불분명해지는걸 막기위해 클래스들을 나누고 추상클래스, 상속 등을 통해 의존성과 결합도를 낮추고 차후 단위 테스트를 용이하게 하였습니다.

</br>

## 실행방법 & 한번 확인해주세요!

### Config_example.yml
실제 파일은 config.yml 입니다.
로컬에서 실행시 db host 변경해주세요.
```yml
databases:
  host: "db"
  port: 3306
  database: "cafe_service"
  username: "root"
  password: "test1234"
  timezone: "+09:00"

secrets:
  django: "key please"

token:
  scret: "jwt secret"
  referesh_expire_day: 7
  expire_sec: 3600

#한번에 조회할 페이지 수는 설정 파일에 상수로 남겨두었습니다.
page_size:
  page_size: 10
```


### 실행 방법 (로컬)
> ```
>pip install -r requirements.txt
>python manage.py makemigrations
>python manage.py migrate
>python manage.py runserver
>```

### 실행 방법 (docker-compose)
> ```
>cd cafe_service
>docker-compose up -d
>```
## API ENDPOINT
![image](https://user-images.githubusercontent.com/101803254/232319502-9fb915e0-df88-4e65-97e5-0e45c1bdc043.png)
본 프로젝트는 스웨거로 자동 문서화되어있습니다.
http://localhost:8000/swagger/ 에서 확인 가능합니다.

### user

URL|Method|Description|
|------|---|---|
|"user/signup/"|POST|회원가입|
|"user/login/"|POST|로그인 : access Token 이 반환되며 헤더에 추가해야 하위 기능들을 이용하실 수 있습니다.|
|"user/logout/"|DELETE|로그아웃 : 헤더에 있는 토큰을 받아 만료시킵니다.|

### "user/login/"

#### request
```
핸드폰 번호는 serializer에서 정규식으로 검증합니다.
#body
{
  "phone": "01012345677",
  "password": "string"
}
```
#### response
```
{
  "meta": {
    "code": 200,
    "message": "반환된 토큰을 헤더에 넣어주세요."
  },
  "data": {
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MywiZXhwIjoxNjgxNjU5NDExLjY2MjMzNX0.LYVluwbKS2L7sXkI1SSOlQamqeajLFKsyjtqw_RlNT4"
  }
}
```

### "user/signup/"
#### request
핸드폰 번호는 serializer에서 정규식으로 검증합니다.
```
{
  "name": "string",
  "phone": "01012341234",
  "password": "string"
}
```
#### response
```{
  "meta": {
    "code": 201,
    "message": "회원가입이 완료되었습니다"
  },
  "data": {
    "id": 5,
    "created_at": "2023-04-16T23:37:30.371157",
    "updated_at": "2023-04-16T23:37:30.372158",
    "password": "$2b$12$K3lamnaB2mFHIZkD1hZUnuc/vzjdI.OzB98f2pcuozAGRi2WDWHIq",
    "phone": "01012341234",
    "name": "string"
  }
}
```
### Product
URL|Method|Description|
|------|---|---|
|"product/create/"|POST|물건 생성|
|"product/update/"|PUT|업데이트 : 해당 물품을 업데이트합니다.|
|"product/delete/"|DELETE|삭제 : 물건을 삭제시킵니다.|
|"product/get/"|GET| 단건 조회 : 단건 조회입니다. 자신이 작성한 것만 검색됩니다.|
|"product/page/"|GET| 페이지 조회: 다량 조회 페이지 검색입니다. 검색어, 초성검색을 지원하며 검색어 입력은 옵션입니다.|

해당 물건을 생성합니다. barcode는 13자리 숫자, 유통기한은 "YYYY-MM-DD-HH-mm" 형태입니다. 두 필드 모두 serializer에서 정규식으로 1차 검증합니다.
#### request
```
{
  "name": "string",
  "price": 0,
  "cost": 0,
  "barcode": "1234123412341",
  "expire_date": "2022-11-11-11-11",
  "description": "string",
  "size": "L"
}
```

#### response
```
{
  "meta": {
    "code": 201,
    "message": "상품이 생성되었습니다."
  },
  "data": {
    "id": 89,
    "created_at": "2023-04-16T23:49:26.779282",
    "updated_at": "2023-04-16T23:49:26.779282",
    "name": "string",
    "price": 0,
    "cost": 0,
    "barcode": "1234123412341",
    "expire_date": "2022-11-11T11:11:00",
    "description": "string",
    "size": "L",
    "user": 3
  }
}
```
#### product/update/

#### request
```
{
  "product_id": 89,
  "name": "string",
  "price": 0,
  "cost": 0,
  "barcode": "1234123412341",
  "expire_date": "2022-11-11-11-11",
  "description": "string",
  "size": "L"
}
```
#### response
```
{
  "meta": {
    "code": 202,
    "message": "상품이 업데이트됩니다."
  },
  "data": {
    "id": 89,
    "created_at": "2023-04-16T23:49:26.779282",
    "updated_at": "2023-04-17T00:16:47.376704",
    "name": "string",
    "price": 0,
    "cost": 0,
    "barcode": "1234123412341",
    "expire_date": "2022-11-11T11:11:00",
    "description": "string",
    "size": "L",
    "user": 3
  }
}
```

## product/delete

#### request
http://localhost:8000/product/delete/?product_id=89

#### response

```
{
  "meta": {
    "code": 200,
    "message": "상품 삭제 완료."
  },
  "data": null
}
```

## product/get
http://localhost:8000/product/get/?product_id=88
#### response
```
{
  "meta": {
    "code": 200,
    "message": "상품 조회 완료."
  },
  "data": {
    "id": 88,
    "created_at": "2023-04-16T23:45:41.771641",
    "updated_at": "2023-04-16T23:45:41.771641",
    "name": "string",
    "price": 0,
    "cost": 0,
    "barcode": "1234123412341",
    "expire_date": "2022-11-11T11:11:00",
    "description": "string",
    "size": "L",
    "user": 3
  }
}
```

## product/page

#### request -1 (페이지만 요청시)
http://localhost:8000/product/page/?page=1

#### response -1 
```
{
  "meta": {
    "code": 200,
    "message": "상품 조회 완료."
  },
  "data": [
    [
      {
        "page": "1",
        "page_count": 4
      }
    ],
    [
      {
        "id": 66,
        "created_at": "2023-04-16T11:03:10.975667",
        "updated_at": "2023-04-16T11:03:10.975667",
        "name": "aaaaa",
        "price": 0,
        "cost": 0,
        "barcode": "1234123412341",
        "expire_date": "2023-12-12T12:12:00",
        "description": "string",
        "size": "s",
        "user": 3
      },
  "..."
        {
        "id": 38,
        "created_at": "2023-04-16T09:34:14.744128",
        "updated_at": "2023-04-16T09:34:14.744128",
        "name": "상수수",
        "price": 0,
        "cost": 0,
        "barcode": "1234123412341",
        "expire_date": "2023-12-12T12:12:00",
        "description": "string",
        "size": "s",
        "user": 3
      }
    ]
  ]
}
```
#### request - 2 (검색어)
http://localhost:8000/product/page/?page=1&q=%EB%AF%BC%EC%B4%88
(민초)
#### response - 2 
```
{
  "meta": {
    "code": 200,
    "message": "상품 조회 완료."
  },
  "data": [
    [
      {
        "page": "1",
        "page_count": 1
      }
    ],
    [
      {
        "id": 54,
        "created_at": "2023-04-16T09:56:13.361075",
        "updated_at": "2023-04-16T09:56:13.361075",
        "name": "민초라떼",
        "price": 0,
        "cost": 0,
        "barcode": "1234123412341",
        "expire_date": "2023-12-12T12:12:00",
        "description": "string",
        "size": "s",
        "user": 3
      },
      {
        "id": 55,
        "created_at": "2023-04-16T09:56:13.567737",
        "updated_at": "2023-04-16T09:56:13.567737",
        "name": "민초라떼",
        "price": 0,
        "cost": 0,
        "barcode": "1234123412341",
        "expire_date": "2023-12-12T12:12:00",
        "description": "string",
        "size": "s",
        "user": 3
      },
      {
        "id": 56,
        "created_at": "2023-04-16T09:56:13.790237",
        "updated_at": "2023-04-16T09:56:13.790237",
        "name": "민초라떼",
        "price": 0,
        "cost": 0,
        "barcode": "1234123412341",
        "expire_date": "2023-12-12T12:12:00",
        "description": "string",
        "size": "s",
        "user": 3
      },
      {
        "id": 57,
        "created_at": "2023-04-16T09:56:13.890580",
        "updated_at": "2023-04-16T09:56:13.890580",
        "name": "민초라떼",
        "price": 0,
        "cost": 0,
        "barcode": "1234123412341",
        "expire_date": "2023-12-12T12:12:00",
        "description": "string",
        "size": "s",
        "user": 3
      },
      {
        "id": 58,
        "created_at": "2023-04-16T09:56:13.994711",
        "updated_at": "2023-04-16T09:56:13.994711",
        "name": "민초라떼",
        "price": 0,
        "cost": 0,
        "barcode": "1234123412341",
        "expire_date": "2023-12-12T12:12:00",
        "description": "string",
        "size": "s",
        "user": 3
      }
    ]
  ]
}
```

#### request -3 (초성)
http://localhost:8000/product/page/?page=1&q=%E3%84%B9%E3%84%B8
(ㄹㄸ)
#### response -3 
```
{
  "meta": {
    "code": 200,
    "message": "상품 조회 완료."
  },
  "data": [
    [
      {
        "page": "1",
        "page_count": 2
      }
    ],
    [
      {
        "id": 54,
        "created_at": "2023-04-16T09:56:13.361075",
        "updated_at": "2023-04-16T09:56:13.361075",
        "name": "민초라떼",
        "price": 0,
        "cost": 0,
        "barcode": "1234123412341",
        "expire_date": "2023-12-12T12:12:00",
        "description": "string",
        "size": "s",
        "user": 3
      },
      {
        "id": 55,
        "created_at": "2023-04-16T09:56:13.567737",
        "updated_at": "2023-04-16T09:56:13.567737",
        "name": "민초라떼",
        "price": 0,
        "cost": 0,
        "barcode": "1234123412341",
        "expire_date": "2023-12-12T12:12:00",
        "description": "string",
        "size": "s",
        "user": 3
      },
      {
        "id": 56,
        "created_at": "2023-04-16T09:56:13.790237",
        "updated_at": "2023-04-16T09:56:13.790237",
        "name": "민초라떼",
        "price": 0,
        "cost": 0,
        "barcode": "1234123412341",
        "expire_date": "2023-12-12T12:12:00",
        "description": "string",
        "size": "s",
        "user": 3
      },
      {
        "id": 57,
        "created_at": "2023-04-16T09:56:13.890580",
        "updated_at": "2023-04-16T09:56:13.890580",
        "name": "민초라떼",
        "price": 0,
        "cost": 0,
        "barcode": "1234123412341",
        "expire_date": "2023-12-12T12:12:00",
        "description": "string",
        "size": "s",
        "user": 3
      },
      {
        "id": 58,
        "created_at": "2023-04-16T09:56:13.994711",
        "updated_at": "2023-04-16T09:56:13.994711",
        "name": "민초라떼",
        "price": 0,
        "cost": 0,
        "barcode": "1234123412341",
        "expire_date": "2023-12-12T12:12:00",
        "description": "string",
        "size": "s",
        "user": 3
      },
      {
        "id": 65,
        "created_at": "2023-04-16T11:03:10.493477",
        "updated_at": "2023-04-16T11:03:10.493477",
        "name": "슈크림 라떼",
        "price": 0,
        "cost": 0,
        "barcode": "1234123412341",
        "expire_date": "2023-12-12T12:12:00",
        "description": "string",
        "size": "s",
        "user": 3
      },
      {
        "id": 61,
        "created_at": "2023-04-16T10:55:32.946670",
        "updated_at": "2023-04-16T10:55:32.946670",
        "name": "초코라떼",
        "price": 0,
        "cost": 0,
        "barcode": "1234123412341",
        "expire_date": "2023-12-12T12:12:00",
        "description": "string",
        "size": "s",
        "user": 3
      },
      {
        "id": 39,
        "created_at": "2023-04-16T09:55:49.934390",
        "updated_at": "2023-04-16T09:55:49.934390",
        "name": "카페라떼",
        "price": 0,
        "cost": 0,
        "barcode": "1234123412341",
        "expire_date": "2023-12-12T12:12:00",
        "description": "string",
        "size": "s",
        "user": 3
      },
      {
        "id": 40,
        "created_at": "2023-04-16T09:55:50.325270",
        "updated_at": "2023-04-16T09:55:50.325270",
        "name": "카페라떼",
        "price": 0,
        "cost": 0,
        "barcode": "1234123412341",
        "expire_date": "2023-12-12T12:12:00",
        "description": "string",
        "size": "s",
        "user": 3
      },
      {
        "id": 41,
        "created_at": "2023-04-16T09:55:50.549246",
        "updated_at": "2023-04-16T09:55:50.549246",
        "name": "카페라떼",
        "price": 0,
        "cost": 0,
        "barcode": "1234123412341",
        "expire_date": "2023-12-12T12:12:00",
        "description": "string",
        "size": "s",
        "user": 3
      }
    ]
  ]
}
```
## 🛠 개발 조건
### custom_json_response()
데코레이터 custom_json_response() 에서 view 가 리턴하는 딕셔너리를 jsonresponse으로 전환해서 리턴합니다.
```python
def custom_json_response():
    """
    에러 핸들링, 메타데이터 헤더 추가 를 동시에 하는 데코레이터입니다.
    해당 데코레이터 사용시 response를 딕서너리 형태로 바꾸어 주어야 합니다.
    Args:
    dict : {
        code : status
        message : str
        response_data : any
    }
    """

    def decorator(func):
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

    return decorator
```

### logout 
인증은 provider.authProvider 에서 담당합니다.
```python
def logout(self, token: str):
        decoded = self._decode(token)
        return self.create_token(decoded["id"], is_expired=True)

def create_token(self, user_id: str, is_expired: bool = False):
    exp = 0 if is_expired else self._get_curr_sec() + self.expire_sec
    encoded_jwt = jwt.encode(
        {"id": user_id, "exp": exp},
        self.key,
        algorithm="HS256",
    )
    return {"access": encoded_jwt}
```
로그아웃 요청이 들어오면 유효기간이 0인 토큰을 하나 발급하면서 인증을 갱신함과 동시에 기존 토큰을 말소합니다.

### 초성검색

```python
#fuzzy_search.py

CHO_HANGUL = [
    "ㄱ",
    "ㄲ",
    "ㄴ",
    "ㄷ",
    "ㄸ",
    "ㄹ",
    "ㅁ",
    "ㅂ",
    "ㅃ",
    "ㅅ",
    "ㅆ",
    "ㅇ",
    "ㅈ",
    "ㅉ",
    "ㅊ",
    "ㅋ",
    "ㅌ",
    "ㅍ",
    "ㅎ",
]

HANGUL_START_CHARCODE = ord("가")
CHO_PERIOD = int(ord("까") - ord("가"))
JUNG_PERIOD = int(ord("개") - ord("가"))


def combine(cho, jung, jong):
    return chr(HANGUL_START_CHARCODE + cho * CHO_PERIOD + jung * JUNG_PERIOD + jong)


def make_regex_by_cho(search=""):
    regex = reduce(
        lambda acc, cho: acc.replace(
            cho,
            f"[{combine(CHO_HANGUL.index(cho), 0, 0)}-{combine(CHO_HANGUL.index(cho) + 1, 0, -1)}]",
        ),
        CHO_HANGUL,
        search,
    )
    return f"{regex}"
```
에서 들어온 초성을 정규식으로 전환해 리턴합니다. 
```
input : "ㄱㅊ"
return : "[가-깋][차-칳]"
```
그리고 repo 단에서 해당 정규식으로 이름을 필터링 해 리턴합니다.

```python
def find_page(self, user_id: int, search_string: str = None, page=1) -> tuple:
        # page setting
        page_size = Config.page_size["page_size"]
        page_limit = page_size * int(page)
        offset = page_limit - page_size

        # user 인스턴스로 1차 필터링
        user_ins = self.user_repo.get_user_ins(user_id=user_id)
        sqs = self.model.objects.filter(user=user_ins)
        # 검색어 존재시 필터링
        if search_string:
            sqs = sqs.filter(name__icontains=search_string) | sqs.filter(
                name__regex=make_regex_by_cho(search=search_string)
            )
        data_cnt = sqs.count()
        
        pagination = sqs.order_by("name")[offset:page_limit]
        serialized = self.serializer(instance=pagination, many=True).data
        page_count = ceil(data_cnt / page_size)
        context = [{"page": page, "page_count": page_count}]
        return context, serialized
```

### 검증
```python
class ProducUpdateRequestSchema(serializers.Serializer):
    """
    상품 업데이트 요청에 대한 정의입니다.
    """

    product_id = serializers.IntegerField()
    name = serializers.CharField(max_length=20, allow_null=False)
    price = serializers.IntegerField(allow_null=False)
    cost = serializers.IntegerField(allow_null=False)
    barcode = serializers.CharField(
        max_length=13,
        allow_null=False,
        validators=[RegexValidator(regex="^[0-9]{13}$", message="바코드는 13자리 길이의 숫자입니다.")],
    )
    expire_date = serializers.CharField(
        allow_null=False,
        validators=[
            RegexValidator(
                regex="\d{4}-\d{2}-\d{2}-\d{2}-\d{2}", message="날짜 형식은 yyyy-mm-dd-hh-mm 입니다."
            )
        ],
    )
    description = serializers.CharField()
    size = serializers.CharField(max_length=1)

    def validate_size(self, value: str):
        if Size.has_value(value):
            return value
        else:
            raise serializers.ValidationError("Unkwon size type")
```
대부분은 serializer에서 정규식을 통해 검증합니다. 사이즈는 enum에서 관리합니다.

## 프로젝트 후기
차후 시간이 되어 해당 프로젝트를 고도화 할 수 있는 기회가 생간다면,
테스트코드를 좀더 촘촘하게 작성해서 full test 와 unit 테스트를 확실하게 구현해보겠습니다.
