from django.contrib import admin

# Register your models here.
from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Student)
admin.site.register(models.Teacher)
admin.site.register(models.Group)
admin.site.register(models.GroupTeacherStudent)
admin.site.register(models.Instrument)
admin.site.register(models.InstrumentManager)
admin.site.register(models.Appointment)
admin.site.register(models.Feedback)