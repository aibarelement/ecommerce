import pytest
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.test.client import Client
from rest_framework import status

from seller_products import models, choices
from orders import repos


@pytest.mark.django_db
class OrderReposTest(object):
    order_repos: repos.OrderReposInterface = repos.OrderReposV1()

    @pytest.fixture(autouse=True)
    def loaddata(self, load_fixtures):
        load_fixtures('users.json', 'products.json', 'seller_products.json')

    def test_create_order(self):
        customer = get_user_model().objects.get(phone_number='+77764791670')
        seller_product = models.SellerProduct.objects.get()
        order_items = [
            {'seller_product': seller_product},
        ]
        data = {
            'customer': customer,
            'order_items': order_items,
        }
        order = self.order_repos.create_order(data)

        assert order.order_items.count() == len(order_items)

        total = order.order_items.aggregate(total=Sum('amount'))['total']
        assert total == sum(i['seller_product'].amount for i in order_items)

        assert all(
            i.amount_currency == choices.CurrencyChoices.KZT for i in order.order_items.all()
        )


@pytest.mark.django_db
class OrderViewTest(object):

    @pytest.fixture(autouse=True)
    def loaddata(self, load_fixtures):
        load_fixtures('users.json', 'products.json', 'seller_products.json')

    def test_create_order(self, client: Client):
        client.login(phone_number='+77764791670', password='string123')

        response = client.post('/api/v1/orders/', content_type='application/json', data={
            'order_items': [
                {'seller_product': 1},
            ],
        })

        assert response.status_code == status.HTTP_201_CREATED
