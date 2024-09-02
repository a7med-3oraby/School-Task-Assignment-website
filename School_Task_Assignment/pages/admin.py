from django.contrib import admin
from .models import Task


# Register your models here.
admin.site.register(Task)
admin.site.site_header ='School Task Assignment'
admin.site.site_title ='School Task Assignment'

