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
            regex=r'^user/(?P<pk>{0})/threads/$'.format(uuid_regex),
            view=views.ListUsersThreads.as_view(),
            name='list_threads_by_user',
    ),
    url(
            regex=r'^thread/(?P<pk>{0})/messages/$'.format(uuid_regex),
            view=views.GetCreateMessages.as_view(),
            name='get_create_messages',
    ),
    url(
            regex=r'^user/(?P<pk>{0})/messages/count/$'.format(uuid_regex),
            view=views.UsersMessagesCount.as_view(),
            name='count_user_messages',
    ),
]
