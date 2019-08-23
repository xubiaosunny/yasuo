from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, SMSCode, LocalStorage, Works, WorksComment, WorksQuestion, WorksQuestionReply, \
    Certification, Message
from .db_admin.auth import UserAdmin, SMSCodeAdmin, CertificationAdmin, MessageAdmin
from .db_admin.storage import LocalStorageAdmin
from .db_admin.works import WorksAdmin, WorksCommentAdmin, WorksQuestionAdmin, WorksQuestionReplyAdmin


admin.site.site_title = _("YiQiPing")
admin.site.site_header = _("YiQiPing Management System")

# Register your models here.


# Now register the new UserAdmin...
admin.site.register(CustomUser, UserAdmin)
admin.site.register(Certification, CertificationAdmin)
admin.site.register(SMSCode, SMSCodeAdmin)
admin.site.register(Message, MessageAdmin)

admin.site.register(LocalStorage, LocalStorageAdmin)

admin.site.register(Works, WorksAdmin)
admin.site.register(WorksComment, WorksCommentAdmin)
admin.site.register(WorksQuestion, WorksQuestionAdmin)
admin.site.register(WorksQuestionReply, WorksQuestionReplyAdmin)

# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
