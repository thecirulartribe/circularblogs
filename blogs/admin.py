from django.contrib import admin
from .models import Blog, Subscribe, service, suggestions
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.register(Blog)
admin.site.register(Subscribe, ImportExportModelAdmin)
admin.site.register(service, ImportExportModelAdmin)
admin.site.register(suggestions, ImportExportModelAdmin)