from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Order, OrderItem, Product


class AdminDashboardAnalyticsTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_user(
            username='admin',
            email='admin@example.com',
            password='secret123',
            is_staff=True,
            is_superuser=True,
        )

        self.product_one = Product.objects.create(
            name='Laptop',
            description='A powerful laptop',
            price=Decimal('1000.00'),
            stock=5,
            featured=True,
            brand='Dell',
            category='Electronics',
        )
        self.product_two = Product.objects.create(
            name='Mouse',
            description='Wireless mouse',
            price=Decimal('25.00'),
            stock=0,
            featured=False,
            brand='Logitech',
            category='Accessories',
        )
        self.product_three = Product.objects.create(
            name='Keyboard',
            description='Mechanical keyboard',
            price=Decimal('75.00'),
            stock=3,
            featured=True,
            brand='Razer',
            category='Accessories',
        )

        first_order = Order.objects.create(user=self.admin_user, total_price=Decimal('1000.00'))
        OrderItem.objects.create(order=first_order, product=self.product_one, quantity=2, price=Decimal('500.00'))

        second_order = Order.objects.create(user=self.admin_user, total_price=Decimal('75.00'))
        OrderItem.objects.create(order=second_order, product=self.product_three, quantity=1, price=Decimal('75.00'))

    def test_admin_dashboard_returns_expected_metrics(self):
        self.client.force_login(self.admin_user)

        response = self.client.get(reverse('admin_dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_users'], 1)
        self.assertEqual(response.context['total_orders'], 2)
        self.assertEqual(response.context['total_products'], 3)
        self.assertEqual(response.context['total_revenue'], Decimal('1075.00'))
        self.assertEqual(response.context['out_of_stock_count'], 1)
        self.assertEqual(response.context['featured_count'], 2)

    def test_admin_dashboard_ranks_products_by_sales_volume(self):
        self.client.force_login(self.admin_user)

        response = self.client.get(reverse('admin_dashboard'))

        self.assertEqual(response.status_code, 200)
        product_analytics = response.context['product_analytics']

        self.assertEqual(product_analytics[0]['product'], self.product_one)
        self.assertEqual(product_analytics[0]['quantity_sold'], 2)
        self.assertEqual(product_analytics[1]['product'], self.product_three)
        self.assertEqual(product_analytics[1]['quantity_sold'], 1)


class UserDashboardTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='customer',
            email='customer@example.com',
            password='secret123',
        )

    def test_regular_user_dashboard_shows_their_orders(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('user_dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('orders', response.context)

    def test_password_reset_page_is_available(self):
        response = self.client.get(reverse('password_reset'))

        self.assertEqual(response.status_code, 200)
