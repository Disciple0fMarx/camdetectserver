from django.contrib import admin
from .models import (
    Face,
    LicensePlate,
    ObjectPrediction,
    FacePrediction,
    LicensePlatePrediction
)

# Register your models here.
admin.site.register(Face)
admin.site.register(LicensePlate)
admin.site.register(ObjectPrediction)
admin.site.register(FacePrediction)
admin.site.register(LicensePlatePrediction)
