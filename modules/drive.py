from __future__ import absolute_import
from __future__ import print_function

import os

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

__log__ = '{function:>10}: {message}'

class Drive:
    def __init__(self):
        self.drive = None
        self.auth()

    def auth(self):
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile('mycreds.txt')

        if gauth.credentials is None:
            gauth.CommandLineAuth()
        elif gauth.access_token_expired:
            try:
                gauth.Refresh()
            except:
                gauth.CommandLineAuth()
        else:
            gauth.Authorize()

        gauth.SaveCredentialsFile('mycreds.txt')

        self.drive = GoogleDrive(gauth)

    def ls(self, **kwargs):
        try:
            return self.drive.ListFile({
                'q': '"{id}" in parents and trashed = false'.format(id=kwargs['id'])
            }).GetList()
        except Exception as e:
            print(str(e))

    def search(self, **kwargs):
        try:
            return self.drive.ListFile({
                'q': '"{id}" in parents and title = "{title}" and trashed = false'.format(
                    id=kwargs['id'],
                    title=kwargs['title']
                )
            }).GetList()
        except Exception as e:
            print(str(e))
            return []

    def download(self, task):
        print(__log__.format(function='Download', message=task['title']))
        try:
            file = self.drive.CreateFile({'id': task['id']})
            file.GetContentFile(os.path.join(task['path'], task['title']))
        except Exception as e:
            print(str(e))

    def upload(self, task):
        print(__log__.format(function='Upload', message=task['title']))
        try:
            file = self.drive.CreateFile({
                'title': task['title'],
                'parents': [{
                    'kind': 'drive#fileLink',
                    'id': task['id']
                }]
            })
            file.SetContentFile(os.path.join(task['path'], task['title']))
            file.Upload()
        except Exception as e:
            print(str(e))

    def mkdir(self, **kwargs):
        try:
            folder = self.drive.CreateFile({
                'title': kwargs['title'],
                'parents':  [{'id': kwargs['id']}],
                'mimeType': 'application/vnd.google-apps.folder'
            })
            folder.Upload()
            return folder['id']
        except Exception as e:
            print(str(e))

    def get(self, **kwargs):
        try:
            file = self.drive.CreateFile({'id': kwargs['id']})
            return file
        except Exception as e:
            print(str(e))

    def isdir(self, **kwargs):
        try:
            return kwargs['item']['mimeType'] == 'application/vnd.google-apps.folder'
        except Exception as e:
            print(str(e))
