from datetime import timedelta

from django.contrib.auth import get_user_model

import pytest

import helpers

from django.db.models import Sum
from django.utils import timezone
from rest_framework import status

from seller_products import models, choices
from payments import choices as payment_choices
from orders import repos


@pytest.mark.django_db
class OrderReposTest(object):
    order_repos: repos.OrderReposInterface = repos.OrderReposV1()

    @pytest.fixture(autouse=True)
    def loaddata(self, load_fixtures):
        load_fixtures('users.json', 'products.json', 'seller_products.json')

    @pytest.mark.parametrize('user_id, seller_product_ides', (
        ('6a4496de-a122-4040-95f9-af71b78f9cd2', (1,)),
        ('6a4496de-a122-4040-95f9-af71b78f9cd2', (1, 2)),
    ))
    @pytest.mark.freeze_time('2020-01-01')
    def test_create_order(self, user_id, seller_product_ides):
        user = get_user_model().objects.get(pk=user_id)
        seller_products = models.SellerProduct.objects.filter(id__in=seller_product_ides)
        order_items = [{'seller_product': seller_product} for seller_product in seller_products]
        data = {
            'customer': user,
            'order_items': order_items,
        }
        order, bill = self.order_repos.create_order(data)

        assert order.order_items.count() == len(order_items)

        total = order.order_items.aggregate(total=Sum('amount'))['total']
        assert total == sum(i['seller_product'].amount for i in order_items)

        assert all(
            i.amount_currency == choices.CurrencyChoices.KZT for i in order.order_items.all()
        )

        assert bill.amount == bill.total == total
        assert bill.status == payment_choices.BillStatusChoices.New
        assert bill.expires_at == timezone.now() + timedelta(minutes=30)


@pytest.mark.django_db
class OrderViewTest(object):

    @pytest.fixture(autouse=True)
    def loaddata(self, load_fixtures):
        load_fixtures('users.json', 'products.json', 'seller_products.json')

    @pytest.mark.parametrize('case, user_id, status_code', (
        ('1', '6a4496de-a122-4040-95f9-af71b78f9cd2', status.HTTP_201_CREATED),
        ('2', '6a4496de-a122-4040-95f9-af71b78f9cd2', status.HTTP_201_CREATED),
        ('3', '6a4496de-a122-4040-95f9-af71b78f9cd2', status.HTTP_400_BAD_REQUEST),
        ('4', '6a4496de-a122-4040-95f9-af71b78f9cd2', status.HTTP_400_BAD_REQUEST),
        ('5', '6a4496de-a122-4040-95f9-af71b78f9cd2', status.HTTP_400_BAD_REQUEST),
        ('1', '02ba6926-39e9-4039-b70e-d240dc11f75f', status.HTTP_403_FORBIDDEN),
    ))
    def test_create_order(self, case, user_id, status_code, api_client):
        user = get_user_model().objects.get(pk=user_id)
        data = helpers.load_json_data(f'orders/create_order/{case}')
        response = api_client.post(
            '/api/v1/orders/',
            format='json',
            data=data,
            HTTP_AUTHORIZATION=helpers.access_token(user),
        )

        assert response.status_code == status_code
