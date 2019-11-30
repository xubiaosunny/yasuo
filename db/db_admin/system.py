from django.contrib import admin


class AppUpdateLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'name', 'version', 'is_force', 'create_time')


class PriceSettingsAdmin(admin.ModelAdmin):
    list_display = '__all__'
