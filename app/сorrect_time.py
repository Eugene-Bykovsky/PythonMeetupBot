from datetime import datetime
import pytz

moscow_tz = pytz.timezone('Europe/Moscow')


def format_datetime_to_msk(iso_datetime):
    utc_dt = datetime.fromisoformat(iso_datetime.replace("Z", "+00:00"))
    msk_dt = utc_dt.astimezone(moscow_tz)
    return msk_dt.strftime("%d.%m.%Y %H:%M")
