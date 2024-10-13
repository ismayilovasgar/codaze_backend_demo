from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    bio = models.CharField(max_length=255, blank=True)
    cover_photo = models.ImageField(upload_to="covers/", null=True, blank=True)

    def __str__(self):
        return f"{self.bio}"

    # groups = models.ManyToManyField(
    #     "auth.Group",
    #     related_name="customuser_set",  # Değiştirin
    #     blank=True,
    #     help_text="The groups this user belongs to.",
    #     verbose_name="groups",
    # )

    # user_permissions = models.ManyToManyField(
    #     "auth.Permission",
    #     related_name="customuser_set",  # Değiştirin
    #     blank=True,
    #     help_text="Specific permissions for this user.",
    #     verbose_name="user permissions",
    # )


class Note(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True,related_name="notes")
    title=models.CharField(max_length=100,null=True,blank=True)
    cover_image=models.ImageField(upload_to="images/",null=True,blank=True)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False, null=True, blank=True)

    # This is the string representation of the object
    def __str__(self):
        return self.title
