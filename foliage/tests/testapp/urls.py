from django.conf.urls import include, url

from wagtail import VERSION

if VERSION < (2, 0):
    from wagtail.wagtailcore import urls as wagtail_urls
else:
    from wagtail.core import urls as wagtail_urls


urlpatterns = [
    url(r'', include(wagtail_urls)),
]
