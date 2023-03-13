
def head(file_name):
    with open(file_name) as file:
        while True:
            yield file.readline()


if __name__ == "__main__":
    head_inst = head('idiot.txt')
    while input() != '':
        print(next(head_inst))
