from django.conf.urls.defaults import *
from django.contrib.sites.models import Site

if Site.objects.get_current().domain == 'mjs-publishing.com':
    from project.objetsdart.customer.urls import urlpatterns
elif Site.objects.get_current().domain == 'publish.mjs-publishing.com':
    from project.objetsdart.client.urls import urlpatterns
elif Site.objects.get_current().domain == 'publishing.mjs-svc.com':
    from project.objetsdart.business.urls import urlpatterns
elif Site.objects.get_current().domain == 'callbacks.mjs-publishing.com':
    from project.objetsdart.callbacks.urls import urlpatterns
elif Site.objects.get_current().domain == 'ledger.mjs-publishing.com':
    from project.objetsdart.ledger.urls import urlpatterns
