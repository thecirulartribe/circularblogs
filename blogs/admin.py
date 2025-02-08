from django.contrib import admin
from .models import Blog, Subscribe, service, suggestions, BlogView
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.register(Subscribe, ImportExportModelAdmin)
admin.site.register(service, ImportExportModelAdmin)
admin.site.register(suggestions, ImportExportModelAdmin)
admin.site.register(BlogView)

@admin.register(Blog)
class BlogAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('Title', 'category', 'author', 'views')
    search_fields = ['Title', 'category', 'author']