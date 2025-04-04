from django.db import models
from django.contrib.auth.models import User



class Blog(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    private_blog = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} ,{self.title[:20]}'


class Comment(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} , {self.title[:20]} , {self.blog.title[:20]}'
    

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} , {self.blog.title[:20]}'


class BlogAccess(models.Model):
    giver = models.ForeignKey(User, related_name='giver', on_delete=models.CASCADE)  
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)  
    approved = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.giver.username} give access to {self.receiver.username} '
