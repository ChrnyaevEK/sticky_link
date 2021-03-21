from django.contrib import admin

from application import models


class Admin(admin.ModelAdmin):
    readonly_fields = ('date_of_creation', 'last_update')


admin.site.register(models.Wall, Admin)
admin.site.register(models.SimpleText, Admin)
admin.site.register(models.URL, Admin)
admin.site.register(models.SimpleList, Admin)
admin.site.register(models.Counter, Admin)
admin.site.register(models.SimpleSwitch, Admin)
