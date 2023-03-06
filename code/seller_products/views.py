from rest_framework.viewsets import ModelViewSet

from utils import mixins
from . import serializers, models, permissions


class SellerProductViewSet(mixins.ActionSerializerMixin,
                           mixins.ActionPermissionMixin,
                           ModelViewSet):
    ACTION_SERIALIZERS = {
        'create': serializers.CreateSellerProductSerializer,
        'update': serializers.UpdateSellerProductSerializer,
        'partial_update': serializers.UpdateSellerProductSerializer,
    }
    ACTION_PERMISSIONS = {
        'update': (permissions.IsSellerAndOwner(),),
        'partial_update': (permissions.IsSellerAndOwner(),),
        'destroy': (permissions.IsSellerAndOwner(),),
    }

    serializer_class = serializers.SellerProductSerializer
    queryset = models.SellerProduct.objects.select_related('seller', 'product')
    permission_classes = permissions.IsSellerOrReadOnly,
