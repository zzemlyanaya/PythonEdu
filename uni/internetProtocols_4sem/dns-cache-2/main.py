import argparse
import signal
import sys
from HideousCache import HideousCacheController
from HideousServer import ServerArgs, HideousServer


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--forwarder', type=str, default='8.8.8.8')
    parser.add_argument('-p', '--port', type=int, default=53)
    return parser.parse_args()


def cache_saver(cache_controller: HideousCacheController):
    def saver(signal_id, frame):
        print('Shutting down....')
        print('Saving cache....')
        cache_controller.save_cache()
        print('Server stopped')
        sys.exit()

    return saver


if __name__ == '__main__':
    try:
        controller = HideousCacheController()
        controller.daemon.start()
        signal.signal(signal.SIGINT, cache_saver(controller))

        args = get_args()
        server_args = ServerArgs('127.0.0.1', args.port, args.forwarder, controller.cache)

        HideousServer(server_args).run()
    except PermissionError:
        print('Not enough rights. Try sudo or run as admin')
        exit(1)

# nslookup urfu.ru 127.0.0.1
# nslookup -query=mx mail.ru 127.0.0.1
# nslookup -query=ns urfu.ru 127.0.0.1
# nslookup -query=soa theverge.com 127.0.0.1
# nslookup 5.255.255.70 127.0.0.1
