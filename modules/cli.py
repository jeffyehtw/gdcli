from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import argparse

from modules.upload import Upload
from modules.download import Download

__version__ = '1.0'
__description__ = 'A command line tool for Google Drive'
__epilog__ = 'Report bugs to <yehcj.tw@gmail.com>'
__log__ = '[{function:>10}] {message}'

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
            '-r',
            '--recursive',
            default=False,
            help=''
        )
        parser.add_argument(
            '-t',
            '--threads',
            default=4,
            help=''
        )
        args = parser.parse_args(sys.argv[2:])

        self._download.sync(id=args.id, path='.')
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
            required=True,
            help=''
        )
        parser.add_argument(
            '-r',
            '--recursive',
            required=False,
            help=''
        )
        parser.add_argument(
            '-t',
            '--threads',
            default=4,
            help=''
        )
        args = parser.parse_args(sys.argv[2:])

        self._upload.sync(id=args.parent, path=os.getcwd(), title=args.file)
        self._upload.do(threads=args.threads)