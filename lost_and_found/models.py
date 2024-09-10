# from django.db import models
#
#
# class Item(models.Model):
#     item_image = models.ImageField(upload_to='items/', blank=True, null=True)
#     email = models.EmailField()
#     mobile = models.CharField(max_length=15)
#     item_name = models.CharField(max_length=255)
#     location = models.CharField(max_length=255)
#     time_date = models.CharField(max_length=100)
#     description = models.TextField()
#
#     def __str__(self):
#         return self.item_name


from django.contrib.auth.models import User
from django.db import models


class Item(models.Model):
    item_image = models.ImageField(upload_to='items/', blank=True, null=True)
    email = models.EmailField()
    mobile = models.CharField(max_length=15)
    item_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    time_date = models.CharField(max_length=100)
    description = models.TextField()
    post_time = models.DateTimeField(auto_now_add=True)
    post_status = models.BooleanField(default=False)
    found_by_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.item_name
