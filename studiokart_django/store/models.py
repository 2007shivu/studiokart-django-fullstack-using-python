from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Product(models.Model):
    BRAND_CHOICES = [
        ('Samsung', 'Samsung'),
        ('Apple', 'Apple'),
        ('Sony', 'Sony'),
        ('Other', 'Other'),
    ]
    brand = models.CharField(max_length=50, choices=BRAND_CHOICES, default='Samsung')
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    mrp = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_count = models.PositiveIntegerField(default=15)
    category = models.CharField(max_length=100)
    image_url = models.URLField(max_length=500)
    gallery_urls = models.TextField(
        blank=True,
        default="",
        help_text="Comma-separated image URLs for multi-angle product gallery"
    )
    description = models.TextField()
    specs = models.TextField()
    colors_config = models.CharField(
        max_length=300,
        default="Natural Titanium:#8e8d8a,Desert Titanium:#c5a987,White Titanium:#f2f1ed,Black Titanium:#2c2c2e"
    )
    storage_config = models.CharField(
        max_length=300,
        default="256GB:0,512GB:15000,1TB:35000"
    )
    ram_config = models.CharField(
        max_length=300,
        default="12GB RAM:0,16GB RAM:10000"
    )
    allow_engraving = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def effective_mrp(self):
        return self.mrp if self.mrp > self.price else self.price

    @property
    def discount_percent(self):
        if self.effective_mrp > self.price and self.effective_mrp > 0:
            diff = self.effective_mrp - self.price
            return int(round((diff / self.effective_mrp) * 100))
        return 0

    def get_gallery_list(self):
        urls = [self.image_url]
        if self.gallery_urls:
            for u in self.gallery_urls.split(','):
                clean = u.strip()
                if clean and clean not in urls:
                    urls.append(clean)
        return urls

    def get_colors_list(self):
        result = []
        for item in self.colors_config.split(','):
            if ':' in item:
                cname, chex = item.split(':', 1)
                result.append({'name': cname.strip(), 'hex': chex.strip()})
        return result or [{'name': 'Natural Titanium', 'hex': '#8e8d8a'}]

    def get_storage_list(self):
        result = []
        for item in self.storage_config.split(','):
            if ':' in item:
                label, extra = item.split(':', 1)
                try:
                    extra_val = float(extra.strip())
                except ValueError:
                    extra_val = 0
                result.append({'label': label.strip(), 'extra': extra_val})
        return result or [{'label': '256GB', 'extra': 0}]

    def get_ram_list(self):
        result = []
        for item in self.ram_config.split(','):
            if ':' in item:
                label, extra = item.split(':', 1)
                try:
                    extra_val = float(extra.strip())
                except ValueError:
                    extra_val = 0
                result.append({'label': label.strip(), 'extra': extra_val})
        return result or [{'label': '12GB RAM', 'extra': 0}]

    @property
    def average_rating(self):
        revs = self.reviews.all()
        if not revs.exists():
            return 4.8
        return round(sum(r.rating for r in revs) / revs.count(), 1)

    def __str__(self):
        return f"{self.brand} - {self.name}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product.name} ({self.rating}★) by {self.user.username}"


class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    selected_color = models.CharField(max_length=80, default='Natural Titanium')
    selected_storage = models.CharField(max_length=50, default='256GB')
    selected_ram = models.CharField(max_length=50, default='12GB RAM')
    engraving_text = models.CharField(max_length=40, blank=True, default='')
    custom_unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def unit_price(self):
        return self.custom_unit_price if self.custom_unit_price > 0 else self.product.price

    @property
    def subtotal(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.selected_color}, {self.selected_ram}, {self.selected_storage})"


class Order(models.Model):
    STATUS_CHOICES = [
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    order_number = models.CharField(max_length=30, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    customer_name = models.CharField(max_length=150)
    mobile = models.CharField(max_length=20)
    address = models.TextField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    card_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=60, default='UPI / Cash on Delivery')
    emi_plan = models.CharField(max_length=120, blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Confirmed')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def can_cancel(self):
        if self.status == 'Cancelled':
            return False
        return timezone.now() <= self.created_at + timedelta(hours=24)

    @property
    def hours_left_to_cancel(self):
        remaining = (self.created_at + timedelta(hours=24)) - timezone.now()
        hours = remaining.total_seconds() / 3600
        return max(0, round(hours, 1))

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=150)
    configuration = models.CharField(max_length=240, blank=True, default='')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.price * self.quantity
