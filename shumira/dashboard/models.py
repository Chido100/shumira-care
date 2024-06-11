from django.db import models
from users.models import User


class Item(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    is_expired = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')


    def __str__(self):
        return self.title




