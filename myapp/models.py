from django.db import models
from cloudinary.models import CloudinaryField

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Blog(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField()
    image = CloudinaryField("image", null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_date']
        
    def __str__(self):
        return self.title
    
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email