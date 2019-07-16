from django.contrib import admin
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe


class LocalStorageAdmin(admin.ModelAdmin):
    def preview(self, obj):
        print(obj.type)
        if obj.type.startswith('image'):
            return mark_safe('<img src="%s" width="500px" />' % (obj.get_url(),))
        if obj.type.startswith('video'):
            return mark_safe('<video src="%s" width="500px" controls></video>' % (obj.get_url(),))
        if obj.type.startswith('audio'):
            return mark_safe('<audio src="%s" width="500px" />' % (obj.get_url(),))
        return ''

    preview.short_description = _('Preview')
    preview.allow_tags = True

    list_display = ('id', 'user', 'type', 'file', 'watermarked_filename', 'create_time')
    readonly_fields = ('preview', )