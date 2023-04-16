import datetime
import os
from unittest.mock import patch
import pytest
from django.conf import settings
from django.test import Client
from cafe.repository import ProductRepository
from cafe.models import Product
from cafe.serializers import ProductSerializer
from user.models import User
from exceptions import NotFoundError


@pytest.fixture
def product_repository():
    return ProductRepository()


@pytest.fixture(scope="session")
def django_db_setup():
    settings.DATABASES


@pytest.fixture
def test_product():
    user = User.objects.create(id=1, name="name", phone="01012341234", password="string")
    product = Product.objects.create(
        user=user,
        name="Test Product",
        price=100,
        cost=50,
        barcode="1234123412341",
        expire_date=datetime.datetime.strptime("2024-06-01-11-11", "%Y-%m-%d-%H-%M"),
        description="Test description",
        size="M",
    )
    return product


@pytest.mark.django_db
def test_get_product(product_repository, test_product):
    product_id = test_product.id
    user_id = test_product.user.id
    result = product_repository.get(product_id, user_id)
    expected_data = ProductSerializer(test_product).data
    assert result == expected_data


@pytest.mark.django_db
def test_get_nonexistent_product(product_repository):
    with pytest.raises(NotFoundError):
        product_repository.get(product_id=1, user_id=1)


@pytest.mark.django_db
def test_get_product_by_name(product_repository, test_product):
    product_name = test_product.name
    result = product_repository.get_by_name(product_name)
    expected_data = ProductSerializer(test_product).data
    assert result == expected_data


@pytest.mark.django_db
def test_get_nonexistent_product_by_name(product_repository):
    with pytest.raises(NotFoundError):
        product_repository.get_by_name(product_name="Nonexistent Product")


@pytest.mark.django_db
def test_create_product(product_repository):
    # patch the get_user_ins method to return a user instance with id 1
    User.objects.create(id=1, name="John", phone="01012341234", password="string")
    data = {
        "name": "New Latte",
        "price": 200,
        "cost": 100,
        "barcode": "1234123412341",
        "expire_date": "2024-06-01-11-11",
        "description": "New product description",
        "size": "L",
    }
    result = product_repository.create(data, 1)
    expected_data = ProductSerializer(Product.objects.get(name="New Latte")).data
    assert result == expected_data


@pytest.mark.django_db
def test_update_product(product_repository, test_product):
    user_id = 1
    product_id = test_product.id
    data = {
        "name": "Updated Latte",
        "price": 150,
        "cost": 75,
        "barcode": "1234123412341",
        "expire_date": "2024-06-01-11-11",
        "description": "Updated product description",
        "size": "S",
    }
    result = product_repository.update(data, user_id, product_id)
    updated_product = Product.objects.get(id=product_id)
    expected_data = ProductSerializer(updated_product).data
    assert result == expected_data


@pytest.mark.django_db
def test_update_nonexistent_product(product_repository):
    with pytest.raises(NotFoundError):
        product_repository.update(data={}, user_id=1, product_id=1)


@pytest.mark.django_db
def test_delete_product(product_repository, test_product):
    user_id = test_product.user.id
    product_id = test_product.id
    product_repository.delete(product_id, user_id)
    with pytest.raises(Product.DoesNotExist):
        Product.objects.get(id=product_id)
