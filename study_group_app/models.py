from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Group(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    image = models.ImageField(upload_to='group_images/', blank=True, null=True)  # Image field

    def __str__(self):
        return self.name

    def get_members(self):
        """Get all members of the group."""
        return self.group_members.all()  # Retrieve members associated with this group


class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group_members')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, default='member')  # e.g., 'admin', 'member'

    class Meta:
        unique_together = ('group', 'user')  # Prevents duplicate membership

    def __str__(self):
        return f"{self.user.username} in {self.group.name}"

    def is_admin(self):
        """Check if the user is an admin of the group."""
        return self.role == 'admin'


class Message(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)  # Allow content to be optional
    file = models.FileField(upload_to='group_files/', blank=True, null=True)  # New field for file uploads
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} [{self.timestamp}]: {self.content[:20] or self.file.name}"


class NotificationStudy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='study_notifications')  # Change to avoid conflict
    group_name = models.CharField(max_length=100)  # Store the group name directly
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='notifications')
    message_content = models.TextField()  # Store the message content
    created_at = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} in {self.group_name} - {self.message_content[:20]}"

    def mark_as_read(self):
        """Mark this notification as read."""
        self.is_read = True
        self.save()
