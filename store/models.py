from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.text import Truncator
import markdown


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=10)
    image_url = models.URLField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    brand = models.CharField(max_length=200, blank=True, default='')
    category = models.CharField(max_length=200, blank=True, default='')

    def __str__(self):
        return self.name

    @property
    def description_preview(self):
        rendered = markdown.markdown(self.description, extensions=['extra', 'fenced_code'])
        return mark_safe(Truncator(rendered).words(24, html=True))

    @property
    def description_html(self):
        return mark_safe(markdown.markdown(self.description, extensions=['extra', 'fenced_code']))

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        # Fallback to 'New' if the database hasn't assigned an ID yet
        order_id = self.id if self.id else "New" # pyright: ignore[reportAttributeAccessIssue]
        return f"Order #{order_id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)