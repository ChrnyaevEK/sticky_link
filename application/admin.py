from django.contrib import admin

from application import models

admin.site.register(models.Wall)
admin.site.register(models.SimpleText)
admin.site.register(models.RichText)
admin.site.register(models.URL)
admin.site.register(models.SimpleList)
admin.site.register(models.Counter)
