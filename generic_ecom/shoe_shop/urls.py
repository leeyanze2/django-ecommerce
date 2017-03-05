from . import views

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth.decorators import login_required, permission_required

restful_urlpatterns = [
    url(r'^rest/inventory/$', views.RestInventoryList.as_view()),
    url(r'^rest/order/$', views.RestInventoryOrder.as_view()),
    url(r'^order/(?P<pk>[0-9]+)/$', login_required(views.InventoryOrder.as_view())),
    url(r'^order/delete/(?P<pk>[0-9]+)/$', login_required(views.InventoryOrder.as_view())),
    url(r'^order/edit/(?P<pk>[0-9]+)/$', login_required(views.InventoryOrderUpdate.as_view())),
    url(r'^orders/add/$', login_required(views.InventoryOrderCreate.as_view())),
    url(r'^orders/$', login_required(views.InventoryOrderList.as_view())),
]

restful_urlpatterns = format_suffix_patterns(restful_urlpatterns)


urlpatterns = restful_urlpatterns + []
