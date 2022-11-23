from django.test import TestCase, Client, RequestFactory
from shop.views import PurchaseCreate
from shop.models import Product

factory = RequestFactory()

class IndexTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_webpage_accessibility(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

class PurchaseCreateTestCase(TestCase):
    def setUp(self):
        yacht = Product.objects.create(name="Яхта", price=90000000, amount=1)
        self.id = yacht.id

        self.request_data = {
            "product": self.id,
            "person": "Dimon",
            "address": "LA"
        }

    def test_purchase(self):
        request = factory.post(f"/buy/{self.id}", data=self.request_data)
        response = PurchaseCreate.as_view()(request)

        self.assertEqual(response.status_code, 200)

        yacht = Product.objects.get(name="Яхта")
        self.assertEqual(yacht.amount, 0)

        response = self.client.get('/')
        self.assertTrue("Нет в наличии" in response.content.decode())
