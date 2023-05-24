from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class AIObject(models.Model):
    title = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.title
    
    def train(self):
        pass

    def predict(self):
        pass


class Face(AIObject):
    image = models.ImageField(upload_to='uploads/faces', blank=True, null=True)


class LicensePlate(AIObject):
    image = models.ImageField(upload_to='uploads/license_plates', blank=True, null=True)


class Prediction(models.Model):
    inference_image = models.ImageField(upload_to='uploads/predictions', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        abstract = True


class ObjectPrediction(Prediction):
    pass


class FacePrediction(Prediction):
    face = models.ForeignKey(Face, on_delete=models.CASCADE, blank=True, null=True)


class LicensePlatePrediction(Prediction):
    license_plate = models.ForeignKey(LicensePlate, on_delete=models.CASCADE, blank=True, null=True)
