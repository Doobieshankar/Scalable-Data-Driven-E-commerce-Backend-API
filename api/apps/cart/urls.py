from django.urls import path
from .views import add_to_cart, get_cart, remove_cart_item

urlpatterns = [
    path("add", add_to_cart),
    path("", get_cart),
    path("item/<int:item_id>", remove_cart_item),
]