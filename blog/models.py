import os
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import settings


STATUS_CHOICES = [
     ('d', 'Draft'),
    ('p', 'Published'),
    ('w', 'Withdrawn'),
]

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='images/',default='')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES,default='')    

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def Meta():
        permissions = [('you_can_give_comment','you can give comment')]

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

class Abc(models.Model):
    image = models.ImageField(upload_to='images/',default='')
    comment = models.ForeignKey('blog.Comment', on_delete=models.CASCADE, related_name='comments')


