from django.conf.urls import patterns, url

from datawarriors.views import IndexView

urlpatterns = patterns(
    '',

    url('^.*$', IndexView.as_view(), name='index'),
)
