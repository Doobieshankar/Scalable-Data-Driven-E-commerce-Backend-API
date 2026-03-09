from django.urls import path
from .views import (
    create_product,
    list_products,
    get_product,
    delete_product
)

urlpatterns = [
    path("", list_products),
    path("create/", create_product),
    path("<slug:slug>/", get_product),
    path("delete/<int:id>/", delete_product),
]