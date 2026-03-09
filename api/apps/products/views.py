from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Product, ProductImage
from .serializers import ProductSerializer, ProductCreateSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_product(request):

    if request.user.role != "VENDOR":
        return Response(
            {
                "status": False,
                "message": "Only vendors can create products"
            },
            status=403
        )

    serializer = ProductCreateSerializer(data=request.data)

    if serializer.is_valid():

        product = serializer.save(vendor=request.user)

        images = request.FILES.getlist("images")

        for image in images:
            ProductImage.objects.create(
                product=product,
                image=image
            )

        return Response(
            {
                "status": True,
                "message": "Product created successfully",
                "data": ProductSerializer(product).data
            },
            status=status.HTTP_201_CREATED
        )

    return Response(
        {
            "status": False,
            "errors": serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )

""" @api_view(["GET"])
def list_products(request):

    products = Product.objects.filter(is_active=True)

    serializer = ProductSerializer(products, many=True)

    return Response(
        {
            "status": True,
            "count": products.count(),
            "data": serializer.data
        }
    ) """

@api_view(["GET"])
def list_products(request):

    queryset = Product.objects.filter(is_active=True).select_related(
        "category",
        "brand",
        "vendor"
    ).prefetch_related("images")

    # Filtering
    category = request.GET.get("category")
    brand = request.GET.get("brand")

    if category:
        queryset = queryset.filter(category_id=category)

    if brand:
        queryset = queryset.filter(brand_id=brand)

    # Search
    search = request.GET.get("search")
    if search:
        queryset = queryset.filter(name__icontains=search)

    # Ordering
    ordering = request.GET.get("ordering")
    if ordering:
        queryset = queryset.order_by(ordering)

    paginator = PageNumberPagination()
    paginated_queryset = paginator.paginate_queryset(queryset, request)

    serializer = ProductSerializer(paginated_queryset, many=True)

    return paginator.get_paginated_response(serializer.data)

@api_view(["GET"])
def get_product(request, slug):

    try:
        product = Product.objects.get(slug=slug, is_active=True)
    except Product.DoesNotExist:
        return Response(
            {"status": False, "message": "Product not found"},
            status=404
        )

    serializer = ProductSerializer(product)

    return Response(
        {
            "status": True,
            "data": serializer.data
        }
    )

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_product(request, id):

    try:
        product = Product.objects.get(id=id, vendor=request.user)
    except Product.DoesNotExist:
        return Response(
            {"status": False, "message": "Product not found"},
            status=404
        )

    product.is_active = False
    product.save()

    return Response(
        {
            "status": True,
            "message": "Product deleted successfully"
        }
    )

