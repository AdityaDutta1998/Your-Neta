from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^interests$', views.interests, name='interests'),
    url(r'^mp$', views.mp, name='mp'),
    url(r'^get_mp_rating$', views.get_mp_rating, name='get_mp_rating'),
]