from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UnicodeSetAttribute, UTCDateTimeAttribute, BinaryAttribute
import uuid
import json

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
    active = BinaryAttribute(default=True)
    created_dt = UTCDateTimeAttribute()
    last_updated_dt = UTCDateTimeAttribute()

    def __repr__(self):
        return 'User: id:{}, nick:{}, password:{}, created_dt:{}'.format(self.id, self.nick, self.password, self.created_dt)



# init Model - create table
if not User.exists():
    User.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)
