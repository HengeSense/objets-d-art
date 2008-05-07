from django.conf.urls.defaults import *

urlpatterns = patterns('project.objetsdart.business.views',
    (r'^$', 'index'), #list top priority notifications after links to the below views

    (r'^notifications/$', 'list_notifications'),
    (r'^scores/$', 'list_objets'),
    (r'^score/(?P<id>\d+)/$', 'edit_objet'),
    (r'^coupons/$', 'list_coupons'),
    (r'^coupon/', 'edit_coupon'),
    (r'^coupon/add/$', 'add_coupon'),
    (r'^clients/$', 'list_clients'),
    (r'^client/(?P<user>[a-zA-Z0-9_]+)/$', 'edit_client')
    (r'^applications/$', 'list_applications'),
    (r'^application/(P<user>[a-zA-Z0-9_]+)/$', 'edit_application'),
    (r'^orders/$', 'list_orders'),

    (r'^admin/', include('django.contrib.admin.urls')),
)

