# from decimal import Decimal
#
# from django.contrib.auth import get_user_model
# from django.db.models import Sum
# from django.test import TestCase
#
# from users.choices import UserTypeChoices
# from products.models import Product
# from seller_products.models import SellerProduct
# from seller_products.choices import CurrencyChoices
# from orders.repos import OrderReposInterface, OrderReposV1
#
#
# class OrderTestCase(TestCase):
#     order_repos: OrderReposInterface = OrderReposV1()
#
#     def setUp(self) -> None:
#         customer = get_user_model().objects.create_user(
#             email='customer@mail.com',
#             phone_number='+77764791670',
#         )
#         customer.user_type = UserTypeChoices.Customer
#         customer.save()
#
#         seller = get_user_model().objects.create_user(
#             email='seller@mail.com',
#             phone_number='+77764791669',
#         )
#         seller.user_type = UserTypeChoices.Seller
#         seller.save()

#         product = Product.objects.create(
#             title='product 1',
#             body='some info',
#             data={'data': 'data'},
#         )
#         SellerProduct.objects.create(
#             seller=seller,
#             product=product,
#             amount=Decimal(10000),
#             amount_currency=CurrencyChoices.KZT,
#         )
#
#     def test_create_order(self):
#         customer = get_user_model().objects.get(phone_number='+77764791670')
#         seller_product = SellerProduct.objects.get()
#         order_items = [
#             {'seller_product': seller_product},
#         ]
#         data = {
#             'customer': customer,
#             'order_items': order_items,
#         }
#         order = self.order_repos.create_order(data)
#
#         self.assertEqual(order.order_items.count(), len(order_items))
#
#         total = order.order_items.aggregate(total=Sum('amount'))['total']
#         self.assertEqual(
#             total,
#             sum(i['seller_product'].amount for i in order_items)
#         )
#         self.assertTrue(
#             all(i.amount_currency == CurrencyChoices.KZT for i in order.order_items.all())
#         )
#
#     def test_get_orders(self):
#         self.assertEqual(self.order_repos.get_orders().count() == 1)
