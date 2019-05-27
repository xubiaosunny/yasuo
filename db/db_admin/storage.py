from django.contrib import admin


class LocalStorageAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'file', 'watermarked_filename', 'create_time')
