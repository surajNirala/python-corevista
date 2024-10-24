from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.TextField(max_length=240,default="")
    text = models.TextField(max_length=1000)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.text[:10]}'
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

