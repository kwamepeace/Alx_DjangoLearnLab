from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
    

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField (auto_now_add= True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    


# class Tag(models.Model):
#     name = models.CharField(max_length=50, unique=True)
#     tags = models.ManyToManyField(Post, related_name='tags')

#     def __str__(self):
#         return self.name