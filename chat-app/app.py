from chalice import Chalice

from model import user
import uuid
from datetime import datetime

app = Chalice(app_name='chat-app')


@app.route('/')
def index():
    return {'hello': 'World'}

@app.route('/users')
def users():
    for u in user.User.scan():
        print(u)
    return user.User.dumps()

@app.route('/user/create', methods=['GET', 'POST'])
def create_user():
    new_user = user.User(
        id = str(uuid.uuid1()),
        first_name = "John",
        last_name = "Doe",
        email = "john@doe.com",
        password = "John",
        active = 1,
        rooms = [],
        created_dt = datetime.utcnow(),
        last_updated_dt = datetime.utcnow()
    )
    new_user.save()


# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#

if __name__ == '__main__':
    #create_user()
    users()
