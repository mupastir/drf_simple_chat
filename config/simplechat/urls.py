from django.conf.urls import url
from simplechat import views

app_name = 'api_chat'
uuid_regex = r'[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}'
urlpatterns = [
    # /chat/
    url(
            regex=r'^thread/$',
            view=views.CreateDestroyThread.as_view(),
            name='create_destroy_thread',
    ),
    url(
            regex=r'^threads/user/(?P<pk>{0})/$'.format(uuid_regex),
            view=views.ListUsersThreads.as_view(),
            name='list_threads_by_user',
    ),
]