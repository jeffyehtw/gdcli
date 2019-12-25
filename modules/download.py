from __future__ import absolute_import
from __future__ import print_function

import os
import concurrent.futures
from modules.drive import Drive

class Download:
    def __init__(self):
        self.tasks = []
        self.drive = Drive()

    def sync(self, **kwargs):
        item = self.drive.get(id=kwargs['id'])
        path = os.path.join(kwargs['path'], item['title'])

        if True == self.drive.isdir(item=item):
            if not os.path.exists(path):
                os.makedirs(path)

            drive_items = self.drive.ls(id=kwargs['id'])
            local_items = os.listdir(path)

            for drive_item in drive_items:
                if True == self.drive.isdir(item=drive_item):
                    self.sync(id=drive_item['id'], path=path)
                else:
                    if drive_item['title'] not in local_items:
                        self.tasks.append({
                            'id': drive_item['id'],
                            'path': path,
                            'title': drive_item['title']
                        })
        else:
            if not os.path.exists(path):
                self.tasks.append({
                    'id': kwargs['id'],
                    'path': kwargs['path'],
                    'title': item['title']
                })

    def do(self, **kwargs):
        with concurrent.futures.ThreadPoolExecutor(max_workers=kwargs['threads']) as executor:
            futures = executor.map(self.drive.download, self.tasks)
