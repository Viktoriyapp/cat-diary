from django.contrib import admin

from cats.models import Cat


# Register your models here.

@admin.register(Cat)
class CatAdmin(admin.ModelAdmin):
    list_display = ['name', 'personality', 'birth_date',]
    list_filter = ['personality',]
    search_fields = ['name',]