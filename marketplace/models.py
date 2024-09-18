from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    phone = models.CharField(
        max_length=15,
        default='0000000000',
        validators=[RegexValidator(r'^\+?1?\d{9,15}$',
                                   message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, choices=[
        ('Electronics', 'Electronics'),
        ('Clothing', 'Clothing'),
        ('Home & Garden', 'Home & Garden'),
        ('Sports', 'Sports'),
        ('Automotive', 'Automotive'),
        ('Other', 'Other'),
    ])
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    date_listed = models.DateTimeField(auto_now_add=True)
    availability = models.BooleanField(default=True)

    # Optional Fields
    condition = models.CharField(max_length=50, choices=[
        ('New', 'New'),
        ('Used', 'Used'),
        ('Refurbished', 'Refurbished'),
    ], default='New')
    shipping_details = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.product.name} - {self.id}'


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
