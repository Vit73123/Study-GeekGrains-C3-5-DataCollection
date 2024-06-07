import locale
from datetime import datetime, timedelta
from dateutil.parser import parse

locale.setlocale(locale.LC_ALL, 'ru')
MONTHS = {
    "января": 1,
    "февраля": 2,
    "марта": 3,
    "апреля": 4,
    "мая": 5,
    "июня": 6,
    "июля": 7,
    "августа": 8,
    "сентября": 9,
    "октября": 10,
    "ноября": 11,
    "декабря": 12,
}

def to_date(s: str):
    *date, time = s.split(", ")
    time = parse(time).time()
    today = datetime.now().date()
    if date:
        day, *month = date[0].split()
        if month:
            month = MONTHS[month[0].lower()]
            day = datetime(today.year, month, int(day)).date()
        elif day.lower() == 'вчера':
            day = today - timedelta(days=1)
    else:
        day = today
    return datetime.combine(day, time)


# current_time = datetime.now()
#
# print(current_time.strftime('%x'))
if __name__ == "__main__":
    # to_date("23 мая, 23:56")
    date = to_date("23 мая, 23:56")
    print(date)
    date = to_date("11:19")
    print(date)
    date = to_date("Вчера, 23:55")
    print(date)
    print()

