from django.contrib import admin


class AppUpdateLogAdmin(admin.ModelAdmin):
    list_display = ('source', 'name', 'version', 'is_force', 'create_time')