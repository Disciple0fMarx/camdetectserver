from django.contrib import admin
from .models import (
    Thing,
    Face,
    LicensePlate,
    FacePrediction,
    LicensePlatePrediction
)

# Register your models here.
admin.site.register(Thing)
admin.site.register(Face)
admin.site.register(LicensePlate)
admin.site.register(FacePrediction)
admin.site.register(LicensePlatePrediction)
