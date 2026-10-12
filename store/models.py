from django.db import models
from django.utils import timezone

CATEGORY_CHOICES = (
    ('Luxury', 'Luxury'),
    ('Chronograph', 'Chronograph'),
    ('Sport', 'Sport'),
    ('Classic', 'Classic'),
)

class Product(models.Model):
    name = models.CharField(max_length=150)
    brand = models.CharField(max_length=100, default='Rolex', blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Luxury')
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    is_featured = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.brand} - {self.name}"

ORDER_STATUS_CHOICES = (
    ('Processing', 'Processing'),
    ('Inspected & Dispatched', 'Inspected & Dispatched'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)

class Order(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=50)
    total_price = models.IntegerField(default=0)
    status = models.CharField(max_length=40, choices=ORDER_STATUS_CHOICES, default='Processing')
    tracking_number = models.CharField(max_length=60, blank=True, default='')
    created_at = models.DateTimeField(default=timezone.now)
    is_paid = models.BooleanField(default=True)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name} ({self.status})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    rating = models.IntegerField(default=5)
    title = models.CharField(max_length=150, blank=True, default='')
    comment = models.TextField()
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Review ({self.rating}★) by {self.author} on {self.product.name}"
