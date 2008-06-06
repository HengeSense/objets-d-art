from django.conf.urls.defaults import *

urlpatterns = patterns('project.objetsdart.customer.views',
    (r'^$', 'index'),
    (r'^news/?(?P<page>\d*)/?', 'news'),
    (r'^sales/?$', 'sales'),

    (r'^search/?$', 'simple_search'),
    (r'^powersearch/?$', 'power_search'),

    #(r'^events/?$', 'calendar'), flatpage

    (r'^score/(?P<slug>[a-z\-]+)/$', 'get_objet_by_slug'),
    (r'^composer/(?P<user_name>.+)/$', 'get_creator'),
    (r'^composer/(?P<user_name>.+)/works/$', 'list_by_composer'),
    (r'^composer/(?P<user_name>[^/]+)/contact/?$', 'client_contact'),

    (r'^categories/$', 'list_public_tags'),
    (r'^composers/$', 'list_composers'),
    (r'^(?P<tag>category/.*)$', 'list_by_tag'),
    (r'^(?P<tag>ensemble/.*)$', 'list_by_tag'),
    (r'^(?P<tag>difficulty/\d+)$', 'list_by_tag'),

    (r'^cart/(?<cart_id>\d+)/$', 'handle_cart'),
    (r'^carts/$', 'handle_carts'),
    (r'^createuser/$', 'create_user'),
    (r'^feedback/$', 'handle_feedback'),
)