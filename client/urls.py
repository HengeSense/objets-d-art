from django.conf.urls.defaults import *

urlpatterns = patterns('project.objetsdart.client.views',
    (r'^$', 'index'),

    (r'^scores/$', 'list_scores'),
    (r'^score/(P<id>\d+)/$', 'edit_score'),
    (r'^score/(P<id>\d+)/contract/$', 'view_contract'),
    (r'^score/add$', 'add_score'),
    (r'^coupons/$', 'list_coupons'),
    (r'^coupon/', 'edit_coupon'),
    (r'^coupon/add/$', 'add_coupon'),
    (r'^profile/$', 'edit_profile'),
    (r'^contract/$', 'view_contract'), #if id not passed, view user contract
    (r'^finances/$', 'list_finances'),
    (r'^finance/request_payment/$', 'request_payment'),
)

