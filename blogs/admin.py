from django.contrib import admin
from .models import Blog, Subscribe, service, suggestions, BlogView, BotIP
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.register(Subscribe, ImportExportModelAdmin)
admin.site.register(service, ImportExportModelAdmin)
admin.site.register(suggestions, ImportExportModelAdmin)
admin.site.register(BlogView)

@admin.register(Blog)
class BlogAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('Title', 'category', 'views')
    search_fields = ['Title', 'category']

@admin.register(BotIP)
class BotIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'added_on')
    search_fields = ('ip_address',)
    ordering = ('-added_on',)
