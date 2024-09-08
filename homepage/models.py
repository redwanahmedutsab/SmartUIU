from django.db import models
from django.utils import timezone


class EmailVerification(models.Model):
    email = models.EmailField(unique=True)
    verification_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'verification_codes'

    def save(self, *args, **kwargs):
        # Delete any existing entry with the same email
        EmailVerification.objects.filter(email=self.email).delete()
        # Save the new entry
        super(EmailVerification, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.email} - {self.verification_code}'


class TemporaryUser(models.Model):
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(unique=False)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.username
