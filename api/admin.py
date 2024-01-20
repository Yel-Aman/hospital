from django.contrib import admin
from .models import Specialization, Visit, Patient, Service, Schedule

admin.site.register(Specialization)
admin.site.register(Visit)
admin.site.register(Patient)
admin.site.register(Service)
admin.site.register(Schedule)