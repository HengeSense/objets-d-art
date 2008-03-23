from django.conf.urls.defaults import *

urlpatterns = patterns('project.objetsdart.client.views',
    (r'^$', 'index'),

    (r'^manage', ''),

    (r'^orders', ''),

    (r'^admin/', include('django.contrib.admin.urls')),
)

