from django.urls import path
from .views import link_list, link_create, link_update, link_delete, stream_view, stream_page, check_stream

urlpatterns = [
    path('', stream_view, name='stream'),
    path('stream/<int:link_id>/', stream_view, name='stream_with_link'),
    path('stream-page/', stream_page, name='stream_page'),
    path('check-stream/', check_stream, name='check_stream'),
    path('links/manage/', link_list, name='link_list'),
    path('links/create/', link_create, name='link_create'),
    path('links/update/<int:pk>/', link_update, name='link_update'),
    path('links/delete/<int:pk>/', link_delete, name='link_delete'),
]
