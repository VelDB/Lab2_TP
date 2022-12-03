from django.test import TestCase, Client, RequestFactory
from shop.views import PurchaseCreate
from shop.models import Product, Purchase

factory = RequestFactory()

class IndexTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_webpage_accessibility(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

class PurchaseCreateTestCase(TestCase):
    def setUp(self):
        painting = Product.objects.create(name="Картина", price=100000, amount=5)
        self.painting_id = painting.id

        yacht = Product.objects.create(name="Яхта", price=90000000, amount=1)
        self.yacht_id = yacht.id

        self.request_data_yacht = {
            "product": self.yacht_id,
            "person": "Dimon",
            "address": "LA"
        }

        self.request_data_painting = {
            "product": self.painting_id,
            "person": "Timon",
            "address": "NY"
        }

    def tearDown(self):
        Product.objects.all().delete()
        Purchase.objects.all().delete()

    def test_purchase(self):
        request = factory.post(f"/buy/{self.yacht_id}", data=self.request_data_yacht)
        response = PurchaseCreate.as_view()(request)

        self.assertEqual(response.status_code, 200)

        yacht = Product.objects.get(name="Яхта")
        self.assertEqual(yacht.amount, 0)

        response = self.client.get('/')
        self.assertTrue("Нет в наличии" in response.content.decode())

    def test_multiple_purchase(self):
        request = factory.post(f"/buy/{self.painting_id}", data=self.request_data_painting)
        for i in range(4):
            PurchaseCreate.as_view()(request)

        painting = Product.objects.get(name="Картина")
        self.assertEqual(painting.amount, 1)
