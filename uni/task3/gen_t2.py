import datetime


def gendates(day, month, year):
    date = datetime.date(year, month, day)
    offset = 0
    while True:
        yield date + datetime.timedelta(offset)
        offset += 1


if __name__ == "__main__":
    day, month, year = map(int, input().split())
    gendates_instance = gendates(day, month, year)
    while input() != '':
        print(next(gendates_instance))
