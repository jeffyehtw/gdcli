from __future__ import absolute_import
from __future__ import print_function

import os
import time
import queue
import threading

from modules.download import Download

class Client:
    def __init__(self):
        self.download = Download()

    def run(self, **kwargs):
        self.download.sync(id=kwargs['id'], path='.')
        self.download.do(threads=4)