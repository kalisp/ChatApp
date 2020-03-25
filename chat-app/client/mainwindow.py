# This Python file uses the following encoding: utf-8
import sys, os
import PySide2.QtQml
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QStringListModel, Qt, QUrl, QAbstractListModel, Slot, QObject
from PySide2.QtGui import QGuiApplication
import requests

from model import  RoomModel as rm, PostModel as pm


class Auth(QObject):
    def __init__(self):
        pass

    @classmethod
    @Slot(str, str)
    def login(self, user_name, password):
        print('{}{}'.format(user_name, password)

    @classmethod
    @Slot(str, str, str)
    def register(self, user_name, password, confirm_password):
        print('{}{}{}'.format(user_name, password, confirm_password)

if __name__ == "__main__":
    app = QGuiApplication([])

    engine = PySide2.QtQml.QQmlApplicationEngine()

    room_model = rm.RoomModel()
#    room_model._data.extend([['id_room2', 'room2'], ['id_room3', 'room3']])
    posts_model = pm.PostModel()

    auth = Auth()
    engine.rootContext().setContextProperty("auth",auth)

    engine.rootContext().setContextProperty("room_model",room_model)
    engine.rootContext().setContextProperty("post_model",posts_model)

    engine.load(QUrl("qml/main.qml"))

    if not engine.rootObjects():
       print("noroot")
       sys.exit(-1)

    sys.exit(app.exec_())
