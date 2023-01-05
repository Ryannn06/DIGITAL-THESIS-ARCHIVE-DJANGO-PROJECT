from django.contrib import admin
from .models import thesisDB, ColDept, ColCourse, Registrations

admin.site.register(thesisDB)
admin.site.register(ColDept)
admin.site.register(ColCourse)
admin.site.register(Registrations)