from rest_framework import serializers
from .models import Category, Brand, Product, ProductImage

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"

class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ["id", "image", "is_primary"]

class ProductSerializer(serializers.ModelSerializer):

    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    vendor = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = "__all__"


class ProductCreateSerializer(serializers.ModelSerializer):

    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "brand",
            "name",
            "slug",
            "description",
            "price",
            "stock",
            "is_available",
            "images"
        ]

