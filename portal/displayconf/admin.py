from django.contrib import admin

from . import models

admin.site.register(models.API)
admin.register(models.ApiData)
