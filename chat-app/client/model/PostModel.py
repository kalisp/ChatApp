# This Python file uses the following encoding: utf-8
from PySide2 import QtWidgets
from PySide2 import QtQuick
from PySide2.QtCore import QAbstractListModel, Qt, Slot, QModelIndex
import requests

class PostModel(QAbstractListModel):
    id_role = Qt.UserRole + 1
    content_role = Qt.UserRole + 2
    user_id_role = Qt.UserRole + 3
    room_id_role = Qt.UserRole +4
    liked_by_role = Qt.UserRole + 5
    disliked_by_role = Qt.UserRole + 6
    created_dt_role = Qt.UserRole + 7

    _roles = {id_role : b'id_role',
              content_role: b'content',
              Qt.DisplayRole : b'display'} # b is important because of PYSIDE-703

    def __init__(self, room_id = '9fc0dd64-6a04-11ea-b2d4-28e347aeb22f'):
                QAbstractListModel.__init__(self)
                self.room_id = room_id
                self.refresh_posts(self.room_id)

    def rowCount(self, parent):
        return len(self._data)

    def data(self, index, role):
        ''' Return value from _data for particular Role '''
        if (index.row() >= 0 and
            index.row() < len(self._data) and
            index.column() == 0):
            if (role == Qt.DisplayRole or role == self.content_role):
                return self._data[index.row()]['content']
            if (role == self.id_role):
                return self._data[index.row()]['id']
            if (role == self.room_id_role):
                return self._data[index.row()]['room_id']
            if (role == self.user_id_role):
                return self._data[index.row()]['user_id']
            if (role == self.liked_by_role):
                return self._data[index.row()]['liked_by']
            if (role == self.disliked_by_role):
                return self._data[index.row()]['disliked_by']
            if (role == self.created_dt_role):
                return self._data[index.row()]['created_dt']
        else:
            return None

    @Slot(str)
    def change_room(self, room_id):
        ''' Change room - repopulate posts for that room '''
        self.room_id = room_id
        self._data = []
        self.refresh_posts(self.room_id)
        print(self._data)

        return

    @Slot(str, str)
    def send_post(self, user_id, content):
        ''' Sends post via API, calls get_posts to emit layoutChanged signal '''
        payload = {
                    'room_id' : self.room_id,
                    'user_id' : user_id,
                    'content' : content
        }
        response = requests.post('http://127.0.0.1:8089/add_post', json=payload)
        if str(response.status_code) == '200':
            self.refresh_posts(self.room_id)

        return

    def refresh_posts(self, room_id):
        ''' Refresh self._data with posts from room_id via HTTP API '''
        #TODO - add usage of created_dt, pagination
        print("refresh_posts {}".format(room_id))
        self.layoutAboutToBeChanged.emit()

        url = "http://127.0.0.1:8089/posts/room_id/{}".format(room_id)
        response = requests.get(url)
        print(response)
        self._data = response.json() or []

        self.layoutChanged.emit()

        return


    def roleNames(self):
        ''' Use custom UserRole to store items of a post '''
        return self._roles
