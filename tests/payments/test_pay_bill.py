import pytest
from rest_framework import status


@pytest.mark.django_db
class BillViewTest(object):

    @pytest.fixture(autouse=True)
    def loaddata(self, load_fixtures):
        load_fixtures(
            'users.json', 'products.json', 'seller_products.json', 'orders.json', 'bills.json',
        )

    @pytest.mark.parametrize('bill_id, status_code', (
        ('85e4c898-7d4c-407c-a1ac-d663ba6ebff7', status.HTTP_204_NO_CONTENT),
        ('85e4c898-7d4c-407c-a1ac-d663ba6ebff8', status.HTTP_404_NOT_FOUND),
    ))
    def test_pay_bill(self, bill_id, status_code, api_client):
        response = api_client.post(f'/api/v1/bills/{bill_id}/pay/')

        assert response.status_code == status_code
