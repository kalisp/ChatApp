from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UnicodeSetAttribute, UTCDateTimeAttribute, BooleanAttribute
import uuid
import json
from datetime import datetime
import hashlib

from config import Config

class Room(Model):
    class Meta:
        table_name = 'Room'
        # Specifies the region
        region = 'eu-central-1'
        # Optional: Specify the hostname only if it needs to be changed from the default AWS setting
        host = Config.DYNAMODB_HOST

    id = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute()
    category = UnicodeAttribute(null=True)
    banned_users = UnicodeSetAttribute(null=True)
    joined_users = UnicodeSetAttribute(null=True)
    read_only = BooleanAttribute(default=False)
    created_dt = UTCDateTimeAttribute()
    last_updated_dt = UTCDateTimeAttribute()

    @classmethod
    def get_by_id(cls, id):
        ''' Return by id - primary keys, throws KeyError if not found
            Query returns ResultIterator
        '''
        return next(cls.query(id))

    def set_read_only(self, read_only):
        ''' Set room to read only, eg. archived '''
        self.read_only = read_only
        self.update(actions=[
            Room.read_only.set(self.read_only),
            Room.last_updated_dt.set(datetime.now()),
        ])

    def add_user(self, user_id):
        ''' Add user_id to room, opposite to User.join_room(room_id) '''
        self.joined_users.append(user_id)
        self.update(actions=[
            Room.joined_users.set(self.joined_users),
            Room.last_updated_dt.set(datetime.now()),
        ])

    def kick_user(self, user_id):
        ''' Add user_id to room, opposite to User.join_room(room_id) '''
        self.joined_users.remove(user_id)
        self.update(actions=[
            Room.joined_users.set(self.joined_users),
            Room.last_updated_dt.set(datetime.now()),
        ])

    def number_of_users(self):
        if not self.joined_users:
            return 0
        return len(self.joined_users)

    def __repr__(self):
        return 'Room: id:{}, name:{}, category:{}, created_dt:{}'.format(self.id, self.name, self.category,
                                                                             self.created_dt)


# init Model - create table
if not Room.exists():
    Room.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
