from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UnicodeSetAttribute, UTCDateTimeAttribute, BooleanAttribute
import uuid
import json
from datetime import datetime
import hashlib

from config import Config

class Post(Model):
    class Meta:
        table_name = 'Post'
        # Specifies the region
        region = 'eu-central-1'
        # Optional: Specify the hostname only if it needs to be changed from the default AWS setting
        host = Config.DYNAMODB_HOST

    id = UnicodeAttribute(hash_key=True)
    user_id = UnicodeAttribute()
    room_id = UnicodeAttribute()
    content = UnicodeAttribute()
    liked_by = UnicodeSetAttribute(null=True)
    disliked_by = UnicodeSetAttribute(null=True)
    created_dt = UTCDateTimeAttribute()
    last_updated_dt = UTCDateTimeAttribute()

    def like(self, user_id, liked):
        ''' Mark post as liked/disliked by a user_id '''
        action = None
        if liked:
            if user_id in self.liked_by:
                return
            self.liked_by.append(user_id)
            action = Post.liked_by.set(self.liked_by)
        else:
            if user_id in self.disliked_by:
                return
            self.disliked_by.append(user_id)
            action = Post.disliked_by.set(self.liked_by)

        self.update(actions=[
            action, # ??
            Post.last_updated_dt.set(datetime.now()),
        ])



# init Model - create table
if not Post.exists():
    Post.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)