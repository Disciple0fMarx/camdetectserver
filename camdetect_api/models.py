from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class AIObject(models.Model):
    title = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.title
    
    def train(self):
        pass

    def predict(self):
        pass


class Thing(AIObject):  # YOLOv5
    image = models.ImageField(upload_to='uploads/things')


class Face(AIObject):
    image = models.ImageField(upload_to='uploads/faces')


class LicensePlate(AIObject):
    image = models.ImageField(upload_to='uploads/license_plates')
