from django.conf.urls.defaults import *

urlpatterns = patterns('project.objetsdart.ledger.views',
    (r'^$', 'index'),

    # Display ledger - query string: 'output_format' defaults to HTML, but
    # can also be 'XML', 'LaTeX', 'PDF' or 'CSV'; 'display_negatives' defaults to
    # 'parentheses', but can be '-', 'red', or 'none' (i.e. for two-column);
    # 'type' defaults to 'all', but can be 'sale', 'payment', 'credit',
    # 'expense', or 'purchase'
    (r'^(?P<year>\d{4})/$', 'display_ledger'),
    (r'^(?P<year>\d{4})/q(?P<quarter>[1234])/$', 'display_ledger'),
    (r'^(?P<year>\d{4})/w(?P<week>\d{2})/$', 'display_ledger'),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'display_ledger'),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$', 'display_ledger'),
    (r'^full/?$', 'display_ledger', { 'full': True }),
)
