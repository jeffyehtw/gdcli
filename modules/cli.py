from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import logging
import argparse

from modules.upload import Upload
from modules.download import Download

logger = logging.getLogger('gdcli')
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    fmt='| %(asctime)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

__version__ = '1.0'
__description__ = 'A command line tool for Google Drive'
__epilog__ = 'Report bugs to <yehcj.tw@gmail.com>'

class Cli:
    def __init__(self):
        self._upload = Upload()
        self._download = Download()

        parser = argparse.ArgumentParser(
            description=__description__,
            epilog=__epilog__
        )
        parser.add_argument('command', help='command help')
        parser.add_argument(
            '-v', '-V', '--version',
            action='version',
            help='show version of program',
            version='v{}'.format(__version__)
        )
        args = parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.command):
            print('Unrecongnized command')
            parser.print_help()
            exit()

        getattr(self, args.command)()

    def download(self):
        parser = argparse.ArgumentParser(description='')
        parser.add_argument(
            'id',
            help=''
        )
        parser.add_argument(
            '-p',
            '--path',
            default=os.getcwd(),
            help=''
        )
        parser.add_argument(
            '-t',
            '--threads',
            default=4,
            type=int,
            help=''
        )
        parser.add_argument(
            '-l',
            '--log',
            help=''
        )
        args = parser.parse_args(sys.argv[2:])

        if None == args.log:
            handler = logging.StreamHandler()
        else:
            handler = logging.FileHandler(args.log)

        handler.setFormatter(formatter)
        logger.addHandler(handler)

        self._download.sync(id=args.id, path=args.path)
        self._download.do(threads=args.threads)

    def upload(self):
        parser = argparse.ArgumentParser(description='')
        parser.add_argument(
            'file',
            help=''
        )
        parser.add_argument(
            '-p',
            '--parent',
            default='root',
            help=''
        )
        parser.add_argument(
            '-t',
            '--threads',
            default=4,
            type=int,
            help=''
        )
        parser.add_argument(
            '-l',
            '--log',
            help=''
        )
        args = parser.parse_args(sys.argv[2:])

        if None == args.log:
            handler = logging.StreamHandler()
        else:
            handler = logging.FileHandler(args.log)

        handler.setFormatter(formatter)
        logger.addHandler(handler)

        self._upload.sync(id=args.parent, path=os.getcwd(), title=args.file)
        self._upload.do(threads=args.threads)