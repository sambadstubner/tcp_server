import argparse
import logging
import sys


class ServerHelpFormatter(argparse.HelpFormatter):
    def __init__(
        self,
        prog: str,
        indent_increment: int = 2,
        max_help_position: int = 24,
        width: int | None = None,
    ) -> None:
        super().__init__(prog, indent_increment, max_help_position, width)


class ServerParser(argparse.ArgumentParser):
    help = """tcp_server.py [-h] [-p PORT] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  port to bind to
  -v, --verbose         turn on debugging output"""

    def __init__(self):
        super().__init__(
            formatter_class=ServerHelpFormatter, usage=argparse.SUPPRESS, add_help=False
        )
        self.add_argument("-h", "--help", action="store_true")
        self.add_argument(
            "-p",
            "--port",
            default=8083,
            type=int,
            help="port to bind to",
            required=False,
        )
        self.add_argument(
            "-v",
            "-verbose",
            action="store_true",
            help="turn on debugging output",
            required=False,
        )

        self.parse()

    def parse(self):
        try:
            self.args = self.parse_args()

        except:
            print(self.help)
            sys.exit(0)

        self.handle_help()
        self.handle_verbose()

    def handle_help(self):
        if self.args.help:
            print(self.help)
            sys.exit(0)

    def handle_verbose(self):
        if self.args.v:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.ERROR)


if __name__ == "__main__":
    args = ServerParser().parse_args()
    print(args.port)
