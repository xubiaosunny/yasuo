from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from db.models import CustomUser, SMSCode, Certification


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = '__all__'

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    # password = ReadOnlyPasswordHashField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=False)

    class Meta:
        model = CustomUser
        fields = ('phone', 'password', 'role', 'full_name', 'province', 'city', 'grade', 'work_place', 'is_active', 'is_admin')

    # def clean_password(self):
    #     # Regardless of what the user provides, return the initial value.
    #     # This is done here, rather than on the field, because the
    #     # field does not have access to the initial value
    #     return self.initial["password"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if self.cleaned_data["password1"]:
            user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('phone', 'role', 'full_name', 'is_active', 'is_admin', 'date_joined')
    list_filter = ('is_admin', 'role')
    fieldsets = (
        (None, {'fields': ('phone', )}),
        ('Change Password', {'fields': ('password1', 'password2',)}),
        ('Personal info', {'fields': ('role', 'full_name', 'province', 'city', 'grade', 'work_place',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'is_admin', 'role', 'password1', 'password2')}
        ),
    )
    search_fields = ('phone',)
    ordering = ('date_joined',)
    filter_horizontal = ()

    def has_delete_permission(self, request, obj=None):
        """ 取消后台删除用户功能 """
        return False


class CertificationAdmin(admin.ModelAdmin):
    def certified_file_img(self, obj):
        return mark_safe('<img src="%s" width="500px" />' % (obj.certified_file.get_url(),))

    certified_file_img.short_description = _('Preview')
    certified_file_img.allow_tags = True

    list_display = ('id', 'user', 'id_number', 'status', 'create_time', 'update_time')
    readonly_fields = ['user', 'certified_file_img']
    list_filter = ('status',)


class SMSCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'code', 'send_time')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'class_name', 'class_id', 'is_read')
