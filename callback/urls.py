from django.conf.urls.defaults import *
urlpatterns = patterns('project.objetsdart.callbacks.views',
    (r'^google-redirect/$', 'checkout_redirect'),
    (r'^gc/$', 'google_checkout'),
    (r'^ledger/', include('project.objetsdart.ledger.urls.py')),
    (r'^ajax/$', 'ajax'),
    (r'^notifications/$', 'notifcations'),
    (r'^maintenance/$', 'maintenance'),
)
