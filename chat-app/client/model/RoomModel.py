# This Python file uses the following encoding: utf-8
from PySide2 import QtWidgets
from PySide2 import QtQuick
from PySide2.QtCore import QAbstractListModel, Qt, Slot
import requests


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
