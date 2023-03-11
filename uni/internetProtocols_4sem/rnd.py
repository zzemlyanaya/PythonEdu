import json
import re
import subprocess
import sys
from urllib import request

IP = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")


# Получаем маршрут от "tracert"
def get_route(ip_name):
    with subprocess.Popen(["traceroute", ip_name],
                          shell=True, stdout=subprocess.PIPE) as p:
        returned = p.stdout.readlines()
    if len(returned) == 1:
        sys.exit(returned[0].decode("cp866"))
    return extract_necessary_data(returned)


def extract_necessary_data(returned):
    route = []
    for i in range(len(returned)):
        if returned[i + 1] == b'\r\n':
            route = returned[i + 2: -2]
            break
    return route


# Запрашиваем данные об ip адресе c "ip-api.com"
def request_ip_data(address):
    url = f'http://ip-api.com/json/{address}'
    data = json.load(request.urlopen(url))
    if "as" in data.keys() and data["as"]:
        required = {"as": data["as"].split(' ')[0],
                    "provider": " ".join(data["as"].split(' ')[1:])}
    else:
        required = {"as": '?', "provider": '?'}
    required.update(
        {"country": data["country"] if (
                "country" in data.keys() and data["country"]) else '?'})
    return required


# Пытаемся получить ip адреса узлов из маршрута
def extract_addresses(route):
    ip_addresses = []
    for node in route:
        try:
            ip_addresses.append(IP.search(str(node)).group(0))
        except AttributeError:
            ip_addresses.append(None)
    return ip_addresses


def main():
    # Получаем доменное имя или IP адрес от пользователя
    ip_name = input("Enter address: ")
    if not ip_name:
        sys.exit("Empty input")

    # Получаем маршрут
    route = get_route(ip_name)

    # Получаем IP адреса
    ip_addresses = extract_addresses(route)

    for i in range(len(ip_addresses)):
        if ip_addresses[i]:
            print(i + 1, ip_addresses[i], request_ip_data(ip_addresses[i]))
        else:
            break


if __name__ == "__main__":
    main()