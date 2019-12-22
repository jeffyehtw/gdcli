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
        items = self.drive.ls(id=kwargs['id'])
        for item in items:
            path = os.path.join(kwargs['path'], item['title'])
            print(item['title'])
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                try:
                    if not os.path.exists(path):
                        os.makedirs(path)
                except:
                    print(str(e))
                self.sync(
                    id=item['id'],
                    path=path
                )
            else:
                if not os.path.exists(path):
                    self.tasks.append({
                        'id': item['id'],
                        'path': path
                    })

    def do(self, **kwargs):
        with concurrent.futures.ThreadPoolExecutor(max_workers=kwargs['threads']) as executor:
            futures = executor.map(self.drive.download, self.tasks)
