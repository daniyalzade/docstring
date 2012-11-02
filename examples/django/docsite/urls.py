from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url

urlpatterns = patterns('',
    url(r'^hello/', 'docsite.views.hello'),
    url(r'^bye/', 'docsite.views.bye'),
)
