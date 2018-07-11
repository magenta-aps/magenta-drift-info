from django.conf.urls import url

from . import views

app_name = 'magentadriftinfo'

urlpatterns = [
    url(r'^$', views.DetailView.as_view(), name='detail'),
    url(r'^index/$', views.IndexView.as_view(), name='index'),
    url(r'^customers?/$', views.CustomerIndexView.as_view(), name='customer_index'),
    url(r'^systems?/$', views.SystemIndexView.as_view(), name='system_index'),
    url(r'^servers?/$', views.ServerIndexView.as_view(), name='server_index'),
    url(r'^server/(?P<server>[a-zA-Z0-9 ]+)/$', views.DetailView.as_view(), name='server'),
    url(r'^system/(?P<system>[a-zA-Z0-9 ]+)/$', views.DetailView.as_view(), name='system'),
    url(r'^customer/(?P<customer>[a-zA-Z0-9 ]+)/$', views.DetailView.as_view(), name='customer'),
]
