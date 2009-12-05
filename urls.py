from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'cal.views.default'),
    (r'^(?P<year>\d+)/$', 'cal.views.year_view'),
    (r'^(?P<year>\d+)/next/$', 'cal.views.next_year_view'),
    (r'^(?P<year>\d+)/prev/$', 'cal.views.prev_year_view'),
    (r'^(?P<year>\d+)/(?P<month>\d+)/$', 'cal.views.month_view'),
    (r'^(?P<year>\d+)/(?P<month>\d+)/next/$', 'cal.views.next_month_view'),
    (r'^(?P<year>\d+)/(?P<month>\d+)/prev/$', 'cal.views.prev_month_view'),
    (r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'cal.views.day_view'),
    (r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/week/$', 'cal.views.week_view'),
    (r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/next/$', 'cal.views.next_day_view'),
    (r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/prev/$', 'cal.views.prev_day_view'),
    (r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/week/next/$', 'cal.views.next_week_view'),
    (r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/week/prev/$', 'cal.views.prev_week_view'),
)
