from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.products.models import Product
from .models import CartItem
from .services import get_or_create_cart

from .models import Cart
from .serializers import CartSerializer

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_cart(request):

    product_id = request.data.get("product_id")
    quantity = int(request.data.get("quantity", 1))

    try:
        product = Product.objects.get(id=product_id, is_deleted=False)
    except Product.DoesNotExist:
        return Response({
            "status": False,
            "message": "Product not found"
        }, status=status.HTTP_404_NOT_FOUND)

    if quantity > product.stock:
        return Response({
            "status": False,
            "message": "Not enough stock"
        }, status=status.HTTP_400_BAD_REQUEST)

    cart = get_or_create_cart(request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += quantity

    item.save()

    return Response({
        "status": True,
        "message": "Product added to cart"
    })

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cart(request):

    cart = get_or_create_cart(request.user)

    serializer = CartSerializer(cart)

    return Response({
        "status": True,
        "data": serializer.data
    })

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_cart_item(request, item_id):

    try:
        item = CartItem.objects.get(
            id=item_id,
            cart__user=request.user
        )
    except CartItem.DoesNotExist:
        return Response({
            "status": False,
            "message": "Cart item not found"
        }, status=status.HTTP_404_NOT_FOUND)

    item.delete()

    return Response({
        "status": True,
        "message": "Item removed from cart"
    })

