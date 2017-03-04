from . import views

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

restful_urlpatterns = [
    url(r'^rest/inventory/', views.inventory_list),
    url(r'^rest/order/', views.order),
]

restful_urlpatterns = format_suffix_patterns(restful_urlpatterns)


urlpatterns = restful_urlpatterns + []
