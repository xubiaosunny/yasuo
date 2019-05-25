from django.contrib import admin
from django.contrib.auth.models import Group

from .models import CustomUser, SMSCode
from .db_admin.auth import UserAdmin, SMSCodeAdmin

# Register your models here.


# Now register the new UserAdmin...
admin.site.register(CustomUser, UserAdmin)
admin.site.register(SMSCode, SMSCodeAdmin)

# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
