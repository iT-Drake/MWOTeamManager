from flask_login import current_user

from datetime import datetime
from datetime import timezone
from datetime import timedelta
from pytz import all_timezones
from pytz import timezone as tz
from pytz import utc

from operator import itemgetter

current_timezone = None

def UTC():
    return utc.zone

def UpdateCurrentTimezone():
    global current_timezone
    if current_user.timezone:
        current_timezone = tz(current_user.timezone)
    else:
        current_timezone = timezone.utc

def user_timezone():
    global current_timezone
    if not current_timezone:
        UpdateCurrentTimezone()
    return current_timezone

def Now(local=False):
    date = datetime.now()
    return date.astimezone(user_timezone()) if local else date.astimezone(timezone.utc)

def Today(local=False):
    date = datetime.today()
    return date.astimezone(user_timezone()) if local else date.astimezone(timezone.utc)

def AllTimezones():
    """Returns a list of all available timezones."""
    return all_timezones

def SetUTC(date):
    """Set timezone information for naive date to UTC."""
    return utc.localize(date) if date.tzinfo is None else date

def SetLocal(date):
    """Set timezone information for naive date to local."""
    return user_timezone().localize(date) if date.tzinfo is None else date

def LocalDate(date):
    """Date without a timezone will be considered UTC."""
    # date = date.replace(tzinfo=timezone.utc)
    if date.tzinfo is None:
        date = utc.localize(date)
    return date.astimezone(user_timezone())

def UniversalDate(date):
    """Date without a timezone will be considered local."""
    # date = date.replace(tzinfo=user_timezone())
    if date.tzinfo is None:
        date = user_timezone().localize(date)
    return date.astimezone(timezone.utc)

def TextToDate(text_value):
    """Converts text data represented as YYYY-MM-DDTHH:mm to date."""
    return datetime.strptime(text_value, "%Y-%m-%dT%H:%M")

def Duration(minutes):
    """Returns timedelta object with duration in minutes that can be added to a date."""
    return timedelta(minutes=minutes)

def Sort(dictionaries, key, reverse=False):
    dictionaries.sort(key=itemgetter(key), reverse=reverse)

## ------------------------------------------------------------------------------------------------
##  Forms
## ------------------------------------------------------------------------------------------------

def FormData(form, date_columns=[], boolean_columns=[]):
    """Convert text-based form data into proper data types."""
    data = {}
    for key, value in form.items():
        if key in date_columns:
            data[key] = TextToDate(value)
        elif key in boolean_columns:
            data[key] = True if form[key] else False
        else:
            data[key] = value
    return data
