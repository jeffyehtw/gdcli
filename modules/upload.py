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
        print(kwargs)
        _result = self.drive.search(id=kwargs['id'], title=kwargs['title'])
        path = os.path.join(kwargs['path'], kwargs['title'])
        if os.path.isfile(path):
            if len(_result) == 0:
                self.tasks.append({
                    'id': kwargs['id'],
                    'path': kwargs['path'],
                    'title': kwargs['title']
                })
        else:
            if len(_result) == 0:
                id = self.drive.mkdir(id=kwargs['id'], title=kwargs['title'])
            else:
                id = _result[0]['id']

            items = os.listdir(path)
            for item in items:
                self.sync(id=id, path=path, title=item)

    def do(self, **kwargs):
        print('do')
        for task in self.tasks:
            print(task)
        with concurrent.futures.ThreadPoolExecutor(max_workers=kwargs['threads']) as executor:
            futures = executor.map(self.drive.upload, self.tasks)
