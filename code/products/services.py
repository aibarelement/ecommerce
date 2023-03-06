from typing import Protocol

from django.db.models import QuerySet

from . import models, repos


class ProductServicesInterface(Protocol):

    def get_products(self) -> QuerySet[models.Product]: ...


class ProductServicesV1:
    product_repos: repos.ProductReposInterface = repos.ProductReposV1()

    def get_products(self) -> QuerySet[models.Product]:
        return self.product_repos.get_products()


class ProductImageServicesInterface(Protocol):

    def get_product_images(self) -> QuerySet[models.ProductImage]: ...


class ProductImageServicesV1:
    product_image_repos: repos.ProductImageReposInterface = repos.ProductImageReposV1()

    def get_product_images(self) -> QuerySet[models.ProductImage]:
        return self.product_image_repos.get_product_images()
