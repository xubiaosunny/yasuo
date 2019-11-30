from django.contrib import admin
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe
from django import forms

from db.models import LocalStorage


class LocalStorageCreationForm(forms.ModelForm):

    class Meta:
        model = LocalStorage
        fields = ('file', )

    def save(self, commit=True, user=None):
        file_type = self.cleaned_data['file'].content_type
        self.instance.user = user
        self.instance.type = file_type
        storage = super().save(commit=commit)

        if file_type.startswith('image') or file_type.startswith('video'):
            from utils.tasks import add_watermark
            add_watermark.delay(storage.id)

        if file_type.startswith('audio'):
            from pydub import AudioSegment
            audio = AudioSegment.from_file(storage.file.path)
            storage.duration_seconds = audio.duration_seconds
            storage.save()

        return storage


class LocalStorageAdmin(admin.ModelAdmin):
    def preview(self, obj):
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
    list_filter = ('type', )

    add_form = LocalStorageCreationForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('file', )}
         ),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def save_form(self, request, form, change):
        if change:
            return form.save(commit=False)
        return form.save(commit=False, user=request.user)
