import os
import pytest
from django.conf import settings
from django.test import Client
from cafe.repository import ProductRepository


@pytest.fixture(scope="session")
def django_db_setup():
    settings.configure(
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": "db.sqlite3",
            }
        },
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.admin",
            "cafe_service.cafe",
        ],
    )


@pytest.fixture(scope="module")
def product_repo():
    return ProductRepository()


@pytest.fixture(scope="module")
def client():
    return Client()


def test_create_product(product_repo, client):
    data = {
        "name": "Test Product",
        "price": 10000,
        "cost": 5000,
        "barcode": "1234567890111",
        "expire_date": "2022-01-01-12-12",
        "description": "A test product",
        "size": "L",
    }
    user_id = 1  # You may want to change this depending on your setup
    response = client.post("/api/products/", data=data)
    assert response.status_code == 201
    assert response.json() == product_repo.create(data, user_id)
