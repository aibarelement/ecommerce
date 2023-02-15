from typing import Protocol

from django.db.models import Min, Q, QuerySet

from . import models


class ProductReposInterface(Protocol):

    @staticmethod
    def get_products() -> QuerySet[models.Product]: ...


class ProductReposV1:

    @staticmethod
    def get_products() -> QuerySet[models.Product]:
        return models.Product.objects.annotate(
            min_amount=Min('seller_products__amount', filter=Q(seller_products__is_active=True))
        )


class ProductImageReposInterface(Protocol):

    @staticmethod
    def get_product_images() -> QuerySet[models.ProductImage]: ...


class ProductImageReposV1:

    @staticmethod
    def get_product_images() -> QuerySet[models.ProductImage]:
        return models.ProductImage.objects.all()
