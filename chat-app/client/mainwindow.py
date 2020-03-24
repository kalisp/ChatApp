# This Python file uses the following encoding: utf-8
import sys, os
import PySide2.QtQml
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QStringListModel, Qt, QUrl, QAbstractListModel
from PySide2.QtGui import QGuiApplication
import requests


def get_data():
    #url = "http://country.io/names.json"
    url = "http://127.0.0.1:8089/rooms"
    response = requests.get(url)
    data = sorted(response.json())

    return data

class RoomModel(QAbstractListModel):
    id_role = Qt.UserRole + 1
    name_role = Qt.UserRole + 2

    _roles = {id_role : b'id_role', name_role: b'name_role', Qt.DisplayRole : b'display'} # b is important because of PYSIDE-703

    def __init__(self):
        QAbstractListModel.__init__(self)
        self._data = self.get_rooms()

    def rowCount(self, parent):
        return len(self._data)

    def data(self, index, role):
        ''' Return value from _data for particular Role '''
        if (
            index.row() >= 0 and
            index.row() < len(self._data) and
             index.column() == 0):
            if (role == self.name_role or role == Qt.DisplayRole):
                return self._data[index.row()][1]
            if (role == self.id_role):
                return self._data[index.row()][0]
        else:
            return None

    def get_rooms(self):
        ''' Returns list of arrays (API return it as array instead of tuple) [id, name] '''
        url = "http://127.0.0.1:8089/rooms"
        response = requests.get(url)
        return response.json() or []

    def roleNames(self):
        return self._roles

class PostModel(QAbstractListModel):
    id_role = Qt.UserRole + 1
    content_role = Qt.UserRole + 2

    _roles = {id_role : b'id_role', content_role: b'content', Qt.DisplayRole : b'display'} # b is important because of PYSIDE-703

    def __init__(self, room_id = '9fc0dd64-6a04-11ea-b2d4-28e347aeb22f'):
                QAbstractListModel.__init__(self)

                self._data = self.get_posts(room_id)

    def rowCount(self, parent):
        return len(self._data)

    def data(self, index, role):
        ''' Return value from _data for particular Role '''
        if (index.row() >= 0 and
            index.row() < len(self._data) and
            index.column() == 0):
            if (role == Qt.DisplayRole or role == self.content_role):
                return self._data[index.row()][1]
            if (role == self.id_role):
                return self._data[index.row()][0]
        else:
            return None

    def get_posts(self, room_id):
        url = "http://127.0.0.1:8089/posts/room_id/{}".format(room_id)
        print('url {}'.format(url))
        response = requests.get(url)
        self._data = response.json() or []
        print('posts: {}'.format(self._data))
        #self.layoutChanged.emit()

    def roleNames(self):
        return self._roles

if __name__ == "__main__":
    app = QGuiApplication([])

    engine = PySide2.QtQml.QQmlApplicationEngine()

    room_model = RoomModel()
#    room_model._data.extend([['id_room2', 'room2'], ['id_room3', 'room3']])
    posts_model = PostModel()

    engine.rootContext().setContextProperty("room_model",room_model)
    engine.rootContext().setContextProperty("post_model",room_model)

    engine.load(QUrl("main.qml"))

    if not engine.rootObjects():
       print("noroot")
       sys.exit(-1)

    sys.exit(app.exec_())
