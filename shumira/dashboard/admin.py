from django.contrib import admin
from .models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_created']
    search_fields = ['title']


admin.site.register(Item, ItemAdmin)


