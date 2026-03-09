from django.db import models
from core.models import BaseModel

from django.utils.text import slugify
import uuid

class Category(BaseModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = "categories"
        indexes = [
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.name

class Brand(BaseModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        db_table = "brands"

    def __str__(self):
        return self.name

from django.conf import settings


class Product(BaseModel):

    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="products"
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products"
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    description = models.TextField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.PositiveIntegerField(default=0)

    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = "products"
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["price"]),
            models.Index(fields=["created_at"]),
        ]

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name) + "-" + str(uuid.uuid4())[:8]

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductImage(BaseModel):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="products/")

    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = "product_images"


