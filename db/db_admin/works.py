from django.contrib import admin


class WorksAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type', 'storage', 'summary', 'create_time', 'location', 'is_delete')


class WorksCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'works', 'user', 'voice', 'is_pay', 'create_time', 'update_time')


class WorksQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'works', 'to', 'question', 'is_pay', 'create_time')


class WorksQuestionReplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'works_question', 'voice', 'create_time')
