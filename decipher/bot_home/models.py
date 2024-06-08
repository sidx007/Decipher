from django.db import models
from django.contrib.auth.models import User

class AuthenticationId(models.Model):
    user_mail = models.OneToOneField(User, on_delete=models.CASCADE)
    integration_key = models.CharField(max_length=255)
    page_title = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.user_mail.username}"
    
class Page(models.Model):
    user_mail = models.ForeignKey(AuthenticationId,related_name="pages", on_delete=models.CASCADE)
    page_name = models.CharField(max_length=255, default="New Page", )
    page_token = models.CharField(max_length=255, default="New Token")
    def __str__(self):
        return f"{self.page_name}"