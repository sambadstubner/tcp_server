import argparse

class ServerParser(argparse.ArgumentParser):
    def __init__(self):
        super().__init__(add_help=False)
        self.add_argument('-h', '--help', action='help')
        self.add_argument('-p', '--port', default=8083, type=int, help="port to bind to", required=False)
        self.add_argument('-v', '-verbose', action='store_true', help="turn on debugging output", required=False)


if __name__ == '__main__':
    args = ServerParser().parse_args()
    print(args.port)

