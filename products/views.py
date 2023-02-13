from django.db.models import Min, Q
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from utils import mixins
from . import serializers, models, permissions


class ProductImageViewSet(ModelViewSet):
    serializer_class = serializers.ProductImageSerializer
    queryset = models.ProductImage.objects.all()


class ProductViewSet(mixins.ActionSerializerMixin, ModelViewSet):
    ACTION_SERIALIZERS = {
        'retrieve': serializers.RetrieveProductSerializer,
    }
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.annotate(
        min_amount=Min('seller_products__amount', filter=Q(seller_products__is_active=True))
    )

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return AllowAny(),

        return permissions.IsMe(),
    
    def list(self, request, *args, **kwargs):
        print(type(request.user))
        
        return super().list(request, *args, **kwargs)
