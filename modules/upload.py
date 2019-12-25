from __future__ import absolute_import
from __future__ import print_function

import os
import concurrent.futures
from modules.drive import Drive

class Upload:
    def __init__(self):
        self.tasks = []
        self.drive = Drive()

    def sync(self, **kwargs):
        path = os.path.join(kwargs['path'], kwargs['title'])
        result = self.drive.search(id=kwargs['id'], title=kwargs['title'])

        if True == os.path.isdir(path):
            if 0 == len(result):
                id = self.drive.mkdir(id=kwargs['id'], title=kwargs['title'])
            else:
                id = result[0]['id']

            local_items = os.listdir(path)
            drive_items = self.drive.ls(id=id)
            drive_items_titles = [x['title'] for x in drive_items]

            for local_item in local_items:
                if True == os.path.isdir(os.path.join(path, local_item)):
                    self.sync(id=id, path=path, title=local_item)
                else:
                    if local_item not in drive_items_titles:
                        self.tasks.append({
                            'id': id,
                            'path': path,
                            'title': local_item
                        })
        else:
            if 0 == len(result):
                self.tasks.append({
                    'id': kwargs['id'],
                    'path': kwargs['path'],
                    'title': kwargs['title']
                })

    def do(self, **kwargs):
        with concurrent.futures.ThreadPoolExecutor(max_workers=kwargs['threads']) as executor:
            futures = executor.map(self.drive.upload, self.tasks)
