from django.contrib import admin

from activities.models import Activity


# Register your models here.

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'energy_cost',]
    list_filter = ['category', 'energy_cost',]
    search_fields = ['name',]