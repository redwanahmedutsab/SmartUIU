from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='blog_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag, related_name='blogs', blank=True)

    def __str__(self):
        return f'{self.title} by {self.author.first_name} {self.author.last_name}'


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.blog.title}'


class Reply(models.Model):
    comment = models.ForeignKey(Comment, null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    parent_reply = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,
                                     related_name='child_replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.parent_reply:
            return f'Reply by {self.author} on reply {self.parent_reply.id}'
        elif self.comment:
            return f'Reply by {self.author} on comment {self.comment.id}'
        else:
            return f'Reply by {self.author}'

    @property
    def is_nested_reply(self):
        return self.parent_reply is not None

    @property
    def parent(self):
        return self.parent_reply or self.comment


class LikeDislike(models.Model):
    Liked = 'like'
    Disliked = 'dislike'
    REACTION_CHOICES = [
        (Liked, 'Like'),
        (Disliked, 'Dislike'),
    ]

    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=7, choices=REACTION_CHOICES)

    class Meta:
        unique_together = ('blog', 'user')

    def __str__(self):
        return f"{self.user} - {self.reaction} on {self.blog.title}"
