from django.conf.urls import url
from users import views

app_name = 'api_user'
urlpatterns = [
    # /user/
    url(
        regex=r'^details/$',
        view=views.UserListAPIView.as_view(),
        name='details',
    ),
    url(
        regex=r'^edit/$',
        view=views.UserUpdateAPIView.as_view(),
        name='edit',
    ),
    url(
        regex=r'^login/$',
        view=views.UserLoginAPIView.as_view(),
        name='login',
    ),
    url(
        regex=r'^logout/$',
        view=views.UserLogoutAPIView.as_view(),
        name='logout',
    ),
    url(
        regex=r'^registration/$',
        view=views.UserRegisterAPIView.as_view(),
        name='registration',
    )
]
