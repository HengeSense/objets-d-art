from django.conf.urls.defaults import *

urlpatterns = patterns('objetsdart.customer',
    (r'^$', 'frontpage'),
    (r'^news/?(?P<page>\d*)/?', 'news'),

    (r'^simplesearch/?$', 'simple_search'),
    (r'^powersearch/?$', 'power_search'),

    (r'^about/(?P<page>.*)/?$', 'fetch_about'), # check flatpages

    (r'^objet/(?P<id>\d+)/?$', 'get_objet_by_id'),
    (r'^objet/(?P<slug>[a-z\-]+)/?$', 'get_objet_by_slug'),
    (r'^creator/(?P<user_name>.+)/?$', 'get_creator'),
    
    (r'^category/(?P<tag>.*)$', 'list_by_tag', {'prefix': 'category/'}),
    (r'^ensemble/(?P<tag>.*)$', 'list_by_tag', {'prefix': 'ensemble/'}),
    (r'^difficulty/(?P<tag>\d+)$', 'list_by_tag', {'prefix': 'difficulty/'}),

    (r'^.+$', 'smart_list'), # Search clients, objets, or flat-pages:

    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
)
