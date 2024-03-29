from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@lulobank.com', password='12345'):
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        email = 'jchitiva@lulobank.com'
        password = '12345'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        email = 'test@LULObank.com'
        user = get_user_model().objects.create_user(
            email,
            '12345'
        )
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_when_super_user_is_created(self):
        user = get_user_model().objects.create_superuser(
            'jchitiva@lulobank.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Car'
        )

        self.assertEqual(str(tag), tag.name)

    def test_product_str(self):
        product = models.Product.objects.create(
            user=sample_user(),
            code='0000',
            description='This is a new product',
            picture='url:'
        )

        self.assertEqual(str(product), product.code)
