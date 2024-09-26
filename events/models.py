from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse


class Event(models.Model):
    CLUB_CHOICES = [
        ('UIUDC', 'UIU Debate Club'),
        ('UIUCC', 'UIU Cultural Club'),
        ('UIUTFC', 'UIU Theater & Film Club'),
        ('UIUBC', 'UIU Business Club'),
        ('UIUCCL', 'UIU Computer Club'),
        ('UIUEEC', 'UIU Electrical & Electronic Club'),
        ('UIUPC', 'UIU Photography Club'),
        ('UIUSSC', 'UIU Social Services Club'),
        ('UIUSC', 'UIU Sports Club'),
        ('UIUMC', 'UIU MBA Club'),
        ('UIUAF', 'UIU APP FORUM'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    club = models.CharField(max_length=100, choices=CLUB_CHOICES)
    banner = models.ImageField(upload_to='event_banners/', blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    # Storing user information
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')

    class Meta:
        ordering = ['-date', '-time']
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('event_detail', args=[self.slug])


class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')
        verbose_name = "Event Registration"
        verbose_name_plural = "Event Registrations"

    def __str__(self):
        return f"{self.user.username} registered for {self.event.title}"