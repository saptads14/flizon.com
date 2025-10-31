from django.db import models
from django.contrib.auth.models import User  

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)  # Ensure this field is present

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.product.price

from django.utils import timezone
from decimal import Decimal


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    full_name = models.CharField(max_length=200)
    line1 = models.CharField("Address line 1", max_length=255)
    line2 = models.CharField("Address line 2", max_length=255, blank=True)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    pincode = models.CharField(max_length=20)
    phone = models.CharField(max_length=30)
    is_default = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} — {self.line1}, {self.city} ({self.pincode})"

    class Meta:
        ordering = ['-is_default', '-created_at']


class Order(models.Model):
    PAYMENT_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('upi', 'UPI'),
        ('card', 'Card'),
        ('netbank', 'Net Banking'),
    ]

    STATUS_CHOICES = [
        ('placed', 'Placed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=64, unique=True)
    shipping_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='orders')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='placed')

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    cgst = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    sgst = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_number} — {self.user}"

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='+')
    product_name = models.CharField(max_length=255)  # snapshot of product name at time of order
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # price per unit at order time
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name} x {self.quantity} (Order {self.order.order_number})"

    class Meta:
        ordering = ['-created_at']
