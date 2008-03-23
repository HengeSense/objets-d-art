from django.conf.urls.defaults import *

urlpatterns = patterns('project.objetsdart.customer.views',
    (r'^$', 'index'),
    (r'^news/?(?P<page>\d*)/?', 'news'),
    (r'^sales/?$', 'sales'),

    (r'^(simple)?search/?$', 'simple_search'),
    (r'^powersearch/?$', 'power_search'),

    (r'events/?$', 'calendar'),

    (r'^objet/(?P<id>\d+)/?$', 'get_objet_by_id'),
    (r'^objet/(?P<slug>[a-z\-]+)/?$', 'get_objet_by_slug'),
    (r'^(creator|client|artist|composer)/(?P<user_name>.+)/?$', 'get_creator'),

    (r'^category/(?P<tag>.*)$', 'list_by_tag', {'prefix': 'category/'}),
    (r'^ensemble/(?P<tag>.*)$', 'list_by_tag', {'prefix': 'ensemble/'}),
    (r'^difficulty/(?P<tag>\d+)$', 'list_by_tag', {'prefix': 'difficulty/'}),
)
