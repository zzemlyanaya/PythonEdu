import datetime


def gendow(day, month, year):
    weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    date = datetime.date(year, month, day)
    offset = 0
    while True:
        yield weekdays[(date + datetime.timedelta(offset)).isoweekday()-1]
        offset += 1


if __name__ == "__main__":
    day, month, year = map(int, input().split())
    gendow_instance = gendow(day, month, year)
    while input() != '':
        print(next(gendow_instance))
