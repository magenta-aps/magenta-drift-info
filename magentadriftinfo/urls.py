from django.conf.urls import url

from . import views

app_name = 'magentadriftinfo'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^server/(?P<server>[a-zA-Z0-9 ]+)/?$', views.IndexView.as_view(), name='server'),
    url(r'^system/(?P<system>[a-zA-Z0-9 ]+)/?$', views.IndexView.as_view(), name='system'),
    url(r'^customer/(?P<customer>[a-zA-Z0-9 ]+)/?$', views.IndexView.as_view(), name='customer'),
]
