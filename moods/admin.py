from django.contrib import admin

from moods.models import MoodEntry


# Register your models here.

@admin.register(MoodEntry)
class MoodEntryAdmin(admin.ModelAdmin):
    list_display = ['cat', 'date', 'mood']
    list_filter = ['mood', 'energy_level']
    search_fields = ['cat__name',]
    date_hierarchy = 'date'