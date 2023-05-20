from django.contrib import admin
from .models import Thing, Face, LicensePlate

# Register your models here.
admin.site.register(Thing)
admin.site.register(Face)
admin.site.register(LicensePlate)
