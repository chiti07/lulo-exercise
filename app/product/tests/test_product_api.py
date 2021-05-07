from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Product

from product.serializers import ProductSerializer, ProductDetailSerializer

PRODUCT_URL = reverse('product:product-list')


def detail_url(product_id):
    return reverse('product:product-detail', args=[product_id])


def sample_product(user, **params):
    defaults = {
        'code': '0000',
        'description': 'First Product',
        'picture': 'url-picture'
    }
    defaults.update(params)

    return Product.objects.create(user=user, **defaults)


class PublicProductApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PRODUCT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProductApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@lulobank.com',
            '12345'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_product(self):
        sample_product(user=self.user)
        sample_product(user=self.user)

        res = self.client.get(PRODUCT_URL)

        products = Product.objects.all().order_by('-id')
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_products_limited_to_user(self):
        user2 = get_user_model().objects.create_user(
            'test2@lulobank.com',
            '12345'
        )
        sample_product(user=user2)
        sample_product(user=self.user)

        res = self.client.get(PRODUCT_URL)

        products = Product.objects.filter(user=self.user)
        serializer = ProductSerializer(products, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_product_detail(self):
        product = sample_product(user=self.user)

        url = detail_url(product.id)
        res = self.client.get(url)

        serializer = ProductDetailSerializer(product)

        self.assertEqual(res.data, serializer.data)

    def test_create_basec_product(self):
        payload = {
            'code': '0000',
            'description': 'Product Test',
            'picture': 'url-picture'
        }
        res = self.client.post(PRODUCT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(product, key))

    def test_partial_update_product(self):
        product = sample_product(user=self.user)

        payload = {
            'code': '0001',
        }

        url = detail_url(product.id)
        self.client.patch(url, payload)

        product.refresh_from_db()
        self.assertEqual(product.code, payload['code'])

    def test_full_update_product(self):
        product = sample_product(user=self.user)
        payload = {
            'code': '0002',
            'description': 'full update',
            'picture': 'ulr-updated'
        }
        url = detail_url(product.id)
        self.client.put(url, payload)

        product.refresh_from_db()
        self.assertEqual(product.code, payload['code'])
        self.assertEqual(product.description, payload['description'])
        self.assertEqual(product.picture, payload['picture'])
