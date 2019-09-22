from django.urls import path

from api.views import auth, user, storage, works, home, pay

urlpatterns = [
    path('auth/send_sms_code/', auth.SendCodeView.as_view()),
    path('auth/token/', auth.TokenView.as_view()),
    path('auth/certification/', auth.CertificationView.as_view()),

    path('user/info/', user.UserInfoView.as_view()),
    path('user/follow/', user.UserFollowView.as_view()),
    path('user/cities/', user.UserCityView.as_view()),
    path('user/grades/', user.UserGradeView.as_view()),
    path('user/all_workspace_of_teachers/', user.UserAllWorkspaceOfTeacherView.as_view()),
    path('user/teachers_of_workspace/', user.UserTeacherOfWorkspaceView.as_view()),
    path('user/<int:_id>/works/', user.UserWorksView.as_view()),
    path('user/follow/teacher', user.UserFollowTeacherView.as_view()),
    path('user/follow/student', user.UserFollowStudentView.as_view()),
    path('user/follow/works', user.UserFollowWorksView.as_view()),
    path('user/message/', user.UserMessageView.as_view()),
    path('user/message/<int:_id>/mark_read/', user.UserMessageReadView.as_view()),
    path('user/message/<int:_id>/chat_detail/', user.UserMessageChartDetailView.as_view()),
    path('user/question/', user.UserQuestionView.as_view()),
    path('user/question/<int:_id>/details/', user.UserQuestionDetailsView.as_view()),

    path('storage/local_storage/', storage.LocalStorageView.as_view()),

    path('works/', works.WorksView.as_view()),
    path('works/category/', works.WorksCategoryView.as_view()),
    path('works/<int:_id>/favorite/', works.WorksFavoriteView.as_view()),
    path('works/<int:_id>/comment/', works.WorksCommentView.as_view()),
    path('works/<int:_id>/question/', works.WorksQuestionView.as_view()),
    path('works/question/', works.WorksDirectQuestionView.as_view()),
    path('works/question/<int:_id>/reply', works.WorksQuestionReplyView.as_view()),

    path('home/', home.IndexView.as_view()),

    path('order/', pay.OrderPayView.as_view()),
    # path('order/check_pay/', pay.CheckPayView.as_view()),
    path('order/alipay_notifiy/', pay.AliPayNotifyView.as_view()),
    path('order/extract_amount/', pay.ExtractPayVIew.as_view()),
    path('order/extract_notify/', pay.AliExtractPayNotifyView.as_view()),
    path('order/payment_record', pay.PayInfo.as_view()),
    path('order/cash_withdrawal', pay.ExtractPayInfo.as_view()),

]
