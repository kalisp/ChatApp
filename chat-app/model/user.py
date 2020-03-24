from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UnicodeSetAttribute, UTCDateTimeAttribute, BooleanAttribute
import uuid
import json
from datetime import datetime
import hashlib

from config import Config

class User(Model):
    class Meta:
        table_name = 'User'
        # Specifies the region
        region = 'eu-central-1'
        # Optional: Specify the hostname only if it needs to be changed from the default AWS setting
        host = Config.DYNAMODB_HOST

    id = UnicodeAttribute(hash_key=True)
    first_name = UnicodeAttribute(null=True)
    last_name = UnicodeAttribute(null=True)
    nick = UnicodeAttribute(null=True)
    email = UnicodeAttribute()
    password = UnicodeAttribute()
    rooms = UnicodeSetAttribute(null=True)
    active = BooleanAttribute(default=True)
    created_dt = UTCDateTimeAttribute()
    last_updated_dt = UTCDateTimeAttribute()

    @classmethod
    def get_by_id(cls, id):
        ''' Return by id - primary keys, throws KeyError if not found'''
        return next(cls.query(id))

    def set_active(self, state):
        self.active = not state
        self.update(actions=[
            User.active.set(self.active),
            User.last_updated_dt.set(datetime.now()),
        ])

    def set_password(self, password):
        self.password = hashlib.sha3_512(password)
        self.update(actions=[
            User.password.set(self.password),
            User.last_updated_dt.set(datetime.now()),
        ])

    def set_nick(self, nick):
        self.nick = nick
        self.update(actions=[
            User.nick.set(self.nick),
            User.last_updated_dt.set(datetime.now()),
        ])

    def join_room(self, room_id):
        ''' Add room_id to 'rooms', opposite to Room.add_user(user_id) '''
        self.rooms.append(room_id)
        self.update(actions=[
            User.rooms.set(self.rooms),
            User.last_updated_dt.set(datetime.now()),
        ])

    def leave_room(self, room_id):
        ''' Remove room_id from 'rooms', opposite to Room.kick_user(user_id) '''
        self.rooms.remove(room_id)
        self.update(actions=[
            User.rooms.set(self.rooms),
            User.last_updated_dt.set(datetime.now()),
        ])

    def get_number_joined_rooms(self):
        return len(self.rooms)

    def __repr__(self):
        return 'User: id:{}, nick:{}, password:{}, created_dt:{}'.format(self.id, self.nick, self.password, self.created_dt)



# init Model - create table
if not User.exists():
    User.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
