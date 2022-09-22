from django.contrib import admin
from app.models import PlentificRecord
# Register your models here.


class PlentificRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'uuid')
admin.site.register(PlentificRecord, PlentificRecordAdmin)