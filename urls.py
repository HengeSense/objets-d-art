from django.conf.urls.defaults import *

urlpatterns = patterns('publishing.customer',
    (r'^$', 'frontpage'),
    (r'^news/?(?P<page>\d*)/?', 'news'),

    (r'^category/(?P<tag>.*)$', 'list_by_tag', {'prefix': 'category/'}),
    (r'^ensemble/(?P<tag>.*)$', 'list_by_tag', {'prefix': 'ensemble/'}),
    (r'^difficulty/(?P<tag>\d+)$', 'list_by_tag', {'prefix': 'difficulty/'}),

    (r'^simplesearch/?$', 'simple_search'),
    (r'^powersearch/?$', 'power_search'),

    (r'^about/(?P<page>.*)/?$', 'fetch_about'), # check flatpages

    (r'^composition/(?P<id>\d+)/?$', 'get_score_by_id'),
    (r'^composition/(?P<slug>.+)/?$', 'get_score_by_slug'),
    (r'^composer/(?P<user_name>.+)/?$', 'get_composer'),

    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
)
