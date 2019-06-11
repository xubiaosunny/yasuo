from django.urls import path

from api.views import auth, user, storage, works, home

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

    path('storage/local_storage/', storage.LocalStorageView.as_view()),

    path('works/', works.WorksView.as_view()),
    path('works/category/', works.WorksCategoryView.as_view()),
    path('works/<int:_id>/favorite/', works.WorksFavoriteView.as_view()),
    path('works/<int:_id>/comment/', works.WorksCommentView.as_view()),
    path('works/<int:_id>/question/', works.WorksQuestionView.as_view()),
    path('works/question/', works.WorksDirectQuestionView.as_view()),

    path('home/', home.IndexView.as_view()),
]
