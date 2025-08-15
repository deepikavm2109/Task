from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.user.username

class Task(models.Model):
    status_choices=[("Pending", "pending"), ("Completed", "completed")]
    title=models.CharField(max_length=100, blank=False, null=False)
    description=models.TextField()
    due_date=models.DateField()
    status=models.CharField(max_length=50, choices=status_choices,default="pending")
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title