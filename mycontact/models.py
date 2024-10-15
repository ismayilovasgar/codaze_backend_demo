from django.db import models


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=15)
    surname = models.CharField(max_length=20)
    email = models.EmailField()
    title = models.CharField(max_length=30)
    content = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.surname} - {self.title}"

    
