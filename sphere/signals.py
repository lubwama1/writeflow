
from django.dispatch import receiver
from django.db.models.signals import post_save 
from notifications.signals import notify
from .models import Comment, Post

@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, created, **kwargs): 
    if created:
        print("Signal triggered for comment:", instance)  
        post = instance.post
        user = instance.author
        #send notification to the post author
        notify.send(sender=user, recipient=post.author, verb='Comment on your post', target=post, description=f'{user.username} commented: {instance.content[:100]}')
