from django.db import models
from users.models import CustomUser


# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver_messages')
    message = models.CharField(max_length=100000, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    audio = models.FileField(upload_to='audios/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'message'

    def __str__(self):
        return f"{self.user.username}-{self.message}"


