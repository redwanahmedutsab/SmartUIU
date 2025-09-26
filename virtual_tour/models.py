from django.db import models


class CampusLocation(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image_360 = models.ImageField(upload_to='360_images/')  # 360° image
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
