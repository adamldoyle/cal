from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from itertools import chain
from cal.models import *
from mixins.helpers import render_with_context
import datetime

def check_date(year, month, day):
    try:
        datetime.date(int(year), int(month), int(day))
    except ValueError:
        raise Http404

def events_for_range(request, start, end):
    events = ScheduledEvent.objects.filter(date__range=(start,end), user=request.user)
    dayList = []
    while start <= end:
        dayList.append([start.year, start.month, start.day, events.filter(date=start)])
        start = start + datetime.timedelta(days=1)
    return dayList

def events_for_range_split(request, startYear, startMonth, startDay, endYear, endMonth, endDay):
    start = datetime.date(int(startYear), int(startMonth), int(startDay))
    end = datetime.date(int(endYear), int(endMonth), int(endDay))
    return events_for_range(request, start, end)

@login_required
def year_view(request, year, template_name='cal/defaults/year_view.html'):
    check_date(year, 1, 1)
    year = int(year)
    start = datetime.date(year, 1, 1)
    end = datetime.date(year+1, 1, 1) + datetime.timedelta(days=-1)
    dayList = events_for_range(request, start, end)
    months = (_('January'), _('February'), _('March'), _('April'), _('May'), _('June'), _('July'), _('August'), _('September'), _('October'), _('November'), _('December'))
    monthList = []
    while len(monthList) < 12:
        day = dayList[0]
        day = datetime.date(day[0], day[1], day[2])
        if day.month == 12:
            days = dayList
        else:
            endTemp = datetime.date(day.year, day.month+1, 1) + datetime.timedelta(days=-1)
            days = dayList[0:endTemp.day]
            del(dayList[0:endTemp.day])
        monthList.append([months[day.month-1], day.weekday(), day.month, days_to_weeks(days)])
    monthList = [monthList[0:4], monthList[4:8], monthList[8:12]]
    years = range(min(year-2,datetime.datetime.today().year-4),max(year+3,datetime.date.today().year+5))
    return render_with_context(request, template_name, {'months': monthList,'year':year, 'years':years, 'title': _('Year View'), 'hide_page_title': True})

def next_year_view(request, year):
    year = int(year) + 1
    return HttpResponseRedirect(reverse('cal.views.year_view', args=(year,)))

def prev_year_view(request, year):
    year = int(year) - 1
    return HttpResponseRedirect(reverse('cal.views.year_view', args=(year,)))

def days_to_weeks(dayList):
    weeks = []
    firstDay = dayList[0]
    weekCount = datetime.date(firstDay[0], firstDay[1], firstDay[2]).weekday()
    week = []
    for count in range(len(dayList)):
        if weekCount % 7 == 0 and weekCount > 0:
            weeks.append([weekCount/7, week])
            week = []
        week.append(dayList[count])
        weekCount = weekCount+1
    weeks.append([weekCount/7, week])
    return weeks

@login_required
def month_view(request, year, month, template_name='cal/defaults/month_view.html'):
    year = int(year)
    month = int(month)
    if month < 1:
        year = year - 1
        month = 12
    if month > 12:
        year = year + 1
        month = 1
    check_date(year, month, 1)
    start = datetime.date(year, month, 1)
    if month == 12:
        end = datetime.date(year+1, 1, 1) + datetime.timedelta(days=-1)
    else:
        end = datetime.date(year, month+1, 1) + datetime.timedelta(days=-1)
    start = start + datetime.timedelta(days=-start.weekday())
    end = end + datetime.timedelta(days=(6-end.weekday()))
    dayList = events_for_range(request, start, end)
    weeks = days_to_weeks(dayList)
    months = (_('January'), _('February'), _('March'), _('April'), _('May'), _('June'), _('July'), _('August'), _('September'), _('October'), _('November'), _('December'))
    years = range(min(year-2,datetime.datetime.today().year-4),max(year+3,datetime.date.today().year+5))
    return render_with_context(request, template_name, {'weeks': weeks, 'year': year, 'month': month, 'years': years, 'months': months, 'title': _('Month View'), 'hide_page_title': True})

def next_month_view(request, year, month):
    month = int(month) + 1
    if month > 12:
        year = int(year) + 1
        month = 1
    return HttpResponseRedirect(reverse('cal.views.month_view', args=(year,month)))

def prev_month_view(request, year, month):
    month = int(month) - 1
    if month < 1:
        year = int(year) - 1
        month = 12
    return HttpResponseRedirect(reverse('cal.views.month_view', args=(year,month)))

@login_required
def day_view(request, year, month, day, template_name='cal/defaults/day_view.html'):
    check_date(year, month, day)
    dayList = events_for_range_split(request, year, month, day, year, month, day)
    return render_with_context(request, template_name, {'days':dayList, 'year':year, 'month':month, 'day':day, 'title': _('Day View'), 'hide_page_title': True })

def next_day_view(request, year, month, day):
    check_date(year, month, day)
    year = int(year)
    month = int(month)
    day = int(day)
    start = datetime.date(year, month, day)
    start = start + datetime.timedelta(days=1)
    return HttpResponseRedirect(reverse('cal.views.day_view', args=(start.year,start.month,start.day)))

def prev_day_view(request, year, month, day):
    check_date(year, month, day)
    year = int(year)
    month = int(month)
    day = int(day)
    start = datetime.date(year, month, day)
    start = start + datetime.timedelta(days=-1)
    return HttpResponseRedirect(reverse('cal.views.day_view', args=(start.year,start.month,start.day)))

@login_required
def week_view(request, year, month, day, template_name='cal/defaults/week_view.html'):
    check_date(year, month, day)
    year = int(year)
    month = int(month)
    day = int(day)
    start = datetime.date(year, month, day)
    start = start + datetime.timedelta(days=-start.weekday())
    end = start + datetime.timedelta(days=6)
    dayList = events_for_range(request, start, end)
    return render_with_context(request, template_name, {'days':dayList, 'year':year, 'month':month, 'day':day, 'title': _('Week View')})

def next_week_view(request, year, month, day):
    check_date(year, month, day)
    year = int(year)
    month = int(month)
    day = int(day)
    start = datetime.date(year, month, day)
    start = start + datetime.timedelta(days=7) + datetime.timedelta(days=-start.weekday())
    return HttpResponseRedirect(reverse('cal.views.week_view', args=(start.year,start.month,start.day)))

def prev_week_view(request, year, month, day):
    check_date(year, month, day)
    year = int(year)
    month = int(month)
    day = int(day)
    start = datetime.date(year, month, day)
    start = start + datetime.timedelta(days=-7) + datetime.timedelta(days=-start.weekday())
    return HttpResponseRedirect(reverse('cal.views.week_view', args=(start.year,start.month,start.day)))

def default(request):
    print 'here'
    today = datetime.date.today()
    return HttpResponseRedirect(reverse('cal.views.month_view', args=(today.year,today.month)))