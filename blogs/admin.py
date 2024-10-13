from django.contrib import admin
from .models import Blog, Subscribe, service, suggestions
from import_export.admin import ImportExportModelAdmin


class BlogAdmin(admin.ModelAdmin):
    list_display = ('Title', 'category', 'author')
    search_fields = ['Title', 'category', 'author']


# Register your models here.
admin.site.register(Blog, ImportExportModelAdmin)
admin.site.register(Subscribe, ImportExportModelAdmin)
admin.site.register(service, ImportExportModelAdmin)
admin.site.register(suggestions, ImportExportModelAdmin)