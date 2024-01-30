from django.contrib import admin

# Register your models here.
from .models import Device, Measurement, ConsolidatedMSE, Process

# Register your models here.
admin.site.register(Process)
admin.site.register(Device)
admin.site.register(Measurement)
admin.site.register(ConsolidatedMSE)
