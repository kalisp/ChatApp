from chalice import Chalice, BadRequestError

from model import user, room, post
import uuid
from datetime import datetime
import hashlib
import json

app = Chalice(app_name='chat-app')

@app.route('/')
def index():
    return {'hello': 'World'}

@app.route('/rooms')
def rooms():
    ''' List all room names '''
    names = []
    for r in room.Room.scan():
        names.append(r.name)
        print(r.name)

    return json.dumps(names)

@app.route('/room/create', methods=['GET', 'POST'])
def create_room():
    ''' Create new room '''
    new_room = room.Room(
        id = str(uuid.uuid1()),
        name = "Room1",
        read_only = False,
        created_dt = datetime.utcnow(),
        last_updated_dt = datetime.utcnow()
    )
    new_room.save()

    return {'200': "Room created"}

@app.route('/room/archive/{id}', methods=['GET', 'POST'])
def archive_room(id):
    ''' Deactivate room, user won't be able to post messages '''
    try:
        r = room.Room(id=id)
        r.set_read_only(True)
    except KeyError:
        raise BadRequestError('Room with id: {} not found'.format(id))

    return {'200' : "Room archived"}

@app.route('/room/num_of_users/{id}', methods=['GET'])
def num_of_users(id):
    try:
        r = room.Room(id=id)
        numb = r.number_of_users()
        return {'200': numb}
    except KeyError:
        raise BadRequestError('Room with id: {} not found'.format(id))

@app.route('/room/add_user/room_id/{room_id}/user_id/{user_id}', methods=['GET', 'POST'])
def add_user(room_id, user_id):
    ''' Deactivate room, user won't be able to post messages '''
    try:
        r = room.Room(id=room_id)
        try:
            u = user.User(id=user_id)
        except KeyError:
            raise BadRequestError('User with id: {} not found'.format(user_id))
        r.add_user(u.id)
        u.join_room(r.id)
    except KeyError:
        raise BadRequestError('Room with id: {} not found'.format(id))

    return {'200' : "Room archived"}

@app.route('/room/kick_user/room_id/{room_id}/user_id/{user_id}', methods=['GET', 'POST'])
def kick_user(room_id, user_id):
    ''' Deactivate room, user won't be able to post messages '''
    try:
        r = room.Room(id=room_id)
        try:
            u = user.User(id=user_id)
        except KeyError:
            raise BadRequestError('User with id: {} not found'.format(user_id))
        r.kick_user(u.id)
        u.leave_room(r.id)
    except KeyError:
        raise BadRequestError('Room with id: {} not found'.format(id))

    return {'200' : "Room archived"}

@app.route('/users')
def users():
    ''' List all users '''
    names = []
    for u in user.User.scan():
        names.append(u.name)

    return json.dumps(names)

@app.route('/user/create', methods=['GET', 'POST'])
def create_user():
    ''' Create new user '''
    new_user = user.User(
        id = str(uuid.uuid1()),
        first_name = "John",
        last_name = "Doe",
        email = "john@doe.com",
        password = hashlib.sha3_512("John"),
        active = 1,
        rooms = [],
        created_dt = datetime.utcnow(),
        last_updated_dt = datetime.utcnow()
    )
    new_user.save()

    return {'200': "User created"}

@app.route('/user/join_room/room_id/{room_id}/user_id/{user_id}', methods=['GET', 'POST'])
def join_room(room_id, user_id): # not sure if needed/wanted
    add_user(room_id, user_id)

@app.route('/user/disable/{id}', methods=['GET', 'POST'])
def disable_user(id):
    ''' Deactivate user, user won't be able to post messages '''
    try:
        us = user.User(id=id)
        us.set_active(False)
    except KeyError:
        raise BadRequestError('User with id: {} not found'.format(id))

    return {'200' : "User deactivated"}

@app.route('/user/activate/{id}', methods=['GET', 'POST'])
def activate_user(id):
    ''' Activate user, user will be able to post messages '''
    try:
        us = user.User(id=id)
        us.set_active(True)
    except KeyError:
        raise BadRequestError('User with id: {} not found'.format(id))

    return {'200' : "User activated"}

@app.route('/user/change_password/{id}/{pass}', methods=['GET', 'POST'])
def change_password(id, password):
    try:
        us = user.User(id=id)
        us.set_password(password) # TODO switch to Cognito!
    except KeyError:
        raise BadRequestError('User with id: {} not found'.format(id))

    return {'200' : "Password changed"}

@app.route('/user/change_nick/{id}/{nick}', methods=['GET', 'POST'])
def change_nick(id, nick):
    try:
        us = user.User(id=id)
        us.set_nick(nick)  # TODO switch to Cognito!
    except KeyError:
        raise BadRequestError('User with id: {} not found'.format(id))

    return {'200' : "Nick changed"}

@app.route('/user/num_of_rooms/{id}', methods=['GET'])
def num_of_rooms(id):
    try:
        us = user.User(id=id)
        numb = us.get_number_joined_rooms()
        return {'200': numb}
    except KeyError:
        raise BadRequestError('User with id: {} not found'.format(id))

# ----------POSTS--------------------
@app.route('/posts/room_id/{room_id}')
def posts(room_id):
    ''' Return all posts for specific room '''
    # TODO add limit, order by created desc
    try:
        r = room.Room(id=id)
        posts  = post.Post(room_id=r.id).scan()
        return json.dumps(posts)
    except KeyError:
        raise BadRequestError('Room with id: {} not found'.format(id))

    return json.dumps(names)

@app.route('/post', methods=['POST'])
def post():
    body = app.current_request.json_body
    try:
        r = room.Room(id=body['room_id'])
        try:
            u = user.User(id=body['user_id'])
        except KeyError:
            raise BadRequestError('User with id: {} not found'.format(body['user_id']))
        r.kick_user(u.id)
        u.leave_room(r.id)
        new_post = post.Post(id = str(uuid.uuid1()),
                         room_id = r.id,
                         user_id = u.id,
                         content = body['content'],
                         created_dt = datetime.utcnow(),
                         last_updated_dt = datetime.utcnow()
                         )
        new_post.save()

        return {'200': new_post.id}
    except KeyError:
        raise BadRequestError('Room with id: {} not found'.format(body['room_id']))

@app.route('/post/id/{post_id}/{type}/user_id/{user_id}')
def posts(post_id, type):
    ''' Like/dislike post_id '''
    try:
        p = post.Post(id=post_id)
        if type == 'like':
            p.like(True)
        elif type == 'dislike':
            p.like(False)
        else:
            raise BadRequestError('Wrong type {} of affection'.format(type))
        return {'200' : 'Post affected'}

    except KeyError:
        raise BadRequestError('Room with id: {} not found'.format(id))

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
    #users()
   #print(disable_user('1bf48208-69f5-11ea-a502-28e347aeb22f'))
    #create_room()
    print(rooms())
