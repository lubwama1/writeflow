
from django.urls import re_path
from . import views

app_name = 'sphere'
urlpatterns = [
    re_path(r'^$', views.home, name='home'),
    re_path(r'^create-post/$', views.create_post, name='create-post'),
    re_path(r'^delete-post/(?P<pk>\d+)/$',
            views.delete_post, name='delete-post'),
    re_path(r'^update-post/(?P<pk>\d+)/$',
            views.update_post, name='update-post'),
    re_path(r'^post-detail/(?P<pk>\d+)/$',
            views.post_detail, name='post-detail'),
    re_path(r'^about/$', views.about_page, name='about'),
    re_path(r'^contact/$', views.contact_page, name='contact'),
    re_path(r'^search/$', views.search_post, name='search'),
    re_path(r'^reply/(?P<pk>\d+)/$',
            views.reply_comment, name='reply'), 
    re_path(r'^notifications/$', views.notification_view, name='notifications'),        
    re_path(r'react/(?P<pk>\d+)/$', views.react_to_post, name='react_to_post'),
]
