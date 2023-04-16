from django.urls import path

from cafe.views import (
    create_product,
    delete_product,
    find_product_page,
    get_product,
    update_product,
)

app_name = "cafe"
urlpatterns = [
    path("product/create/", create_product, name="prorduct_create"),
    path("product/update/", update_product, name="prorduct_update"),
    path("product/get/", get_product, name="prorduct_get"),
    path("product/page/", find_product_page, name="prorduct_find"),
    path("product/delete/", delete_product, name="prorduct_delete"),
]
