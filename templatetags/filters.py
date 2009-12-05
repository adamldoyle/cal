from django import template
register = template.Library()

def format_datetime(format_string, date):
    return date.strftime(str(format_string))
register.simple_tag(format_datetime)

def format_datetime_raw(format_string, year, month=1, day=1, hour=0, minute=0, second=0):
    import datetime
    return format_datetime(format_string, datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), int(second)))
register.simple_tag(format_datetime_raw)