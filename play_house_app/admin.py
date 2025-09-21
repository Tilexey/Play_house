from django.contrib import admin
from .models import *

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

class HallAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity']
    list_filter = ['capacity']
    search_fields = ['name', 'description']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 200px;" />'
        return "No image"
    image_preview.allow_tags = True
    image_preview.short_description = 'Image Preview'

class PlaceAdmin(admin.ModelAdmin):
    list_display = ['number', 'hall', 'category', 'active']
    list_filter = ['hall', 'category', 'active']
    search_fields = ['number', 'hall__name']
    list_editable = ['active']

class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'place', 'date', 'start_time', 'end_time']
    list_filter = ['date', 'place__hall']
    search_fields = ['user__username', 'place__number']
    readonly_fields = ['created_at']
    
    def created_at(self, obj):
        return "Автоматично створено"
    created_at.short_description = 'Створено'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Hall, HallAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Booking, BookingAdmin)