import gen_t2
import gen_t3


def gentuple(day, month, year):
    gendates_inst = gen_t2.gendates(day, month, year)
    gendow_inst = gen_t3.gendow(day, month, year)
    while True:
        date = next(gendates_inst)
        weekday = next(gendow_inst)
        yield date.day, date.month, date.year, weekday


if __name__ == "__main__":
    day, month, year = map(int, input().split())
    gentuple_instance = gentuple(day, month, year)
    while input() != '':
        print(next(gentuple_instance))
