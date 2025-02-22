
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from textwrap import shorten
from django.urls import reverse
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    likes = models.ManyToManyField(
        User, related_name='liked_posts', blank=True)
    reactions = models.JSONField(default=dict)
    def __str__(self) -> str:
        #return self.title[0:50]
        return shorten(self.title, width=50, placeholder='...')
    @property
    def likes_count(self): 
        return self.post.likes.count()
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']
    def get_absolute_url(self):
        return reverse('sphere:post-detail', kwargs={'pk': self.pk})
    
class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField() 
    created_at = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(
        User, related_name='liked_comments', blank=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    @property
    def likes_count(self):
        return self.likes.count()
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['-created_at']
    def get_absolute_url(self):
        return reverse("sphere:post-detail", kwargs={"pk": self.pk})  + f"#comment-{self.pk}"
    

   
class Contact(models.Model):

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Message from {self.full_name} ({self.email})'
    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        ordering = ['-created_at']

