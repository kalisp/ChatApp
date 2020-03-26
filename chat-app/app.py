from chalice import Chalice, BadRequestError, UnauthorizedError

from model import user, room, post
import uuid
from datetime import datetime
import hashlib
import json
import logging

import requests

app = Chalice(app_name='chat-app')
app.log.setLevel(logging.DEBUG)

@app.route('/')
def index():
    return {'hello': 'World'}

@app.route('/rooms')
def rooms():
    ''' List all room names as tuples of (id, name)'''
    app.log.debug("rooms")
    rooms = []
    for r in room.Room.scan():
        rooms.append((r.id, r.name))

    rooms = sorted(rooms, key = lambda i: i[1])

    return json.dumps(rooms)

@app.route('/room/create', methods=['GET', 'POST'])
def create_room():
    ''' Create new room '''
    app.log.debug("create_room")
    new_room = room.Room(
        id = str(uuid.uuid1()),
        name = "Room2",
        read_only = False,
        created_dt = datetime.utcnow(),
        last_updated_dt = datetime.utcnow()
    )
    new_room.save()

    return {'200': "Room created"}

@app.route('/room/archive/{id}', methods=['GET', 'POST'])
def archive_room(id):
    ''' Deactivate room, user won't be able to post messages '''
    app.log.debug("archive_room")
    try:
        r = room.Room.get_by_id(id=id)
        r.set_read_only(True)
    except KeyError:
        raise BadRequestError('1 Room with id: {} not found'.format(id))

    return {'200' : "Room archived"}

@app.route('/room/num_of_users/{id}', methods=['GET'])
def num_of_users(id):
    app.log.debug("num_of_users")
    try:
        r = room.Room.get_by_id(id=id)
        app.log.debug('found room {}'.format(r))
        numb = r.number_of_users()
        return {'200': numb}
    except KeyError:
        raise BadRequestError('2 Room with id: {} not found'.format(id))

@app.route('/room/add_user/room_id/{room_id}/user_id/{user_id}', methods=['GET', 'POST'])
def add_user(room_id, user_id):
    ''' Deactivate room, user won't be able to post messages '''
    app.log.debug("add_user")
    try:
        r = room.Room.get_by_id(id=room_id)
        try:
            u = user.User.get_by_id(id=user_id)
        except KeyError:
            raise BadRequestError('User with id: {} not found'.format(user_id))
        r.add_user(u.id)
        u.join_room(r.id)
    except KeyError:
        raise BadRequestError('3 Room with id: {} not found'.format(id))

    return {'200' : "Room archived"}

@app.route('/room/kick_user/room_id/{room_id}/user_id/{user_id}', methods=['GET', 'POST'])
def kick_user(room_id, user_id):
    ''' Deactivate room, user won't be able to post messages '''
    app.log.debug("kick_user")
    try:
        r = room.Room.get_by_id(id=room_id)
        try:
            u = user.User.get_by_id(id=user_id)
        except KeyError:
            raise BadRequestError('User with id: {} not found'.format(user_id))
        r.kick_user(u.id)
        u.leave_room(r.id)
    except KeyError:
        raise BadRequestError('4 Room with id: {} not found'.format(id))

    return {'200' : "Room archived"}

@app.route('/users')
def users():
    ''' List all users '''
    app.log.debug("users")
    names = []
    for u in user.User.scan():
        names.append((u.id, u.nick))

    return json.dumps(names)

@app.route('/user/login', methods=['POST'])
def login_user():
    app.log.debug("login")
    body = app.current_request.json_body
    app.log.debug("body {}".format(body))
    for u in user.User.scan():
        if u.user_name == body['user_name']:
            print('exist pass{} send pass {}'.format(u.password, hashlib.sha3_512(body['password'].encode('utf-8'))))
            if hashlib.sha3_512(body['password'].encode('utf-8')).hexdigest() == u.password:
                u.set_last_accessed_dt()
                app.log.debug(u.id)
                return {'200' : u.id}
            else:
                raise UnauthorizedError('Wrong password')

    raise BadRequestError('User with id: {} not found'.format(id))

@app.route('/user/create', methods=['GET', 'POST'])
def create_user():
    ''' Create new user '''
    app.log.debug("create_user")
    body = app.current_request.json_body
    app.log.debug(body)
    passw = hashlib.sha3_512(body['password'].encode('utf-8')).hexdigest()
    new_user = user.User(
        id = str(uuid.uuid1()),
        user_name = body['user_name'],
        first_name = body['first_name'],
        last_name = body['last_name'],
        nick = body['nick'],
        email = body['email'],
        password = passw,
        active = 1,
        rooms = [],
        created_dt = datetime.utcnow(),
        last_updated_dt = datetime.utcnow(),
        last_accessed_dt = datetime.utcnow(),
    )
    new_user.save()
    print(new_user.id)

    return {'200': new_user.id}

@app.route('/user/join_room/room_id/{room_id}/user_id/{user_id}', methods=['GET', 'POST'])
def join_room(room_id, user_id): # not sure if needed/wanted
    app.log.debug("join_room")
    add_user(room_id, user_id)

@app.route('/user/disable/{id}', methods=['GET', 'POST'])
def disable_user(id):
    ''' Deactivate user, user won't be able to post messages '''
    app.log.debug("disable_user")
    try:
        us = user.User.get_by_id(id=id)
        us.set_active(False)
    except KeyError:
        raise BadRequestError('User with id: {} not found'.format(id))

    return {'200' : "User deactivated"}

@app.route('/user/activate/{id}', methods=['GET', 'POST'])
def activate_user(id):
    ''' Activate user, user will be able to post messages '''
    app.log.debug("activate_user")
    try:
        us = user.User.get_by_id(id=id)
        us.set_active(True)
    except KeyError:
        raise BadRequestError('User with id: {} not found'.format(id))

    return {'200' : "User activated"}

@app.route('/user/change_password/{id}/{pass}', methods=['GET', 'POST'])
def change_password(id, password):
    app.log.debug("change_password")
    try:
        us = user.User.get_by_id(id=id)
        us.set_password(password) # TODO switch to Cognito!
    except KeyError:
        raise BadRequestError('User with id: {} not found'.format(id))

    return {'200' : "Password changed"}

@app.route('/user/change_nick/{id}/{nick}', methods=['GET', 'POST'])
def change_nick(id, nick):
    app.log.debug("change_nick")
    try:
        us = user.User.get_by_id(id=id)
        us.set_nick(nick)  # TODO switch to Cognito!
    except KeyError:
        raise BadRequestError('User with id: {} not found'.format(id))

    return {'200' : "Nick changed"}

@app.route('/user/num_of_rooms/{id}', methods=['GET'])
def num_of_rooms(id):
    app.log.debug("num_of_rooms")
    try:
        us = user.User.get_by_id(id=id)
        numb = us.get_number_joined_rooms()
        return {'200': numb}
    except KeyError:
        raise BadRequestError('User with id: {} not found'.format(id))

# ----------POSTS--------------------
@app.route('/posts/room_id/{room_id}')
def posts(room_id):
    ''' Return all posts for specific room in json string, sorted by created_dt_timestamp desc '''
    # TODO add limit
    app.log.debug("posts")
    try:
        r = room.Room.get_by_id(id=room_id)
        app.log.debug("room_id {}".format(room_id))
        room_posts  = post.Post.query(r.id)
        response = []
        for p in room_posts:
            response.append(p.to_dict())
        response = sorted(response,
                          key = lambda i: i['created_dt_timestamp'],
                          reverse=True)

        return json.dumps(response)
    except KeyError:
        raise BadRequestError('5 Room with id: {} not found'.format(id))

@app.route('/add_post', methods=['POST', 'PUT'])
def add_post():
    app.log.debug("add_post")
    body = app.current_request.json_body
    try:
        r = room.Room.get_by_id(body['room_id'])

        try:
            u = user.User.get_by_id(body['user_id'])
        except KeyError:
            raise BadRequestError('User with id: {} not found'.format(body['user_id']))
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
        raise BadRequestError('6 Room with id: {} not found'.format(body['room_id']))

@app.route('/post/id/{post_id}/{type}/user_id/{user_id}')
def like_post(post_id, type):
    ''' Like/dislike post_id '''
    app.log.debug("like_post")
    try:
        p = post.Post.get_by_id(id=post_id)
        if type == 'like':
            p.like(True)
        elif type == 'dislike':
            p.like(False)
        else:
            raise BadRequestError('Wrong type {} of affection'.format(type))
        return {'200' : 'Post affected'}

    except KeyError:
        raise BadRequestError('7 Room with id: {} not found'.format(id))

if __name__ == '__main__':
    #create_user()
    #print(users())
    #print(disable_user('1bf48208-69f5-11ea-a502-28e347aeb22f'))
    #create_room()
    #print(rooms())

    # p = posts("9fc0dd64-6a04-11ea-b2d4-28e347aeb22f")
    # print(p)
    # print(type(p))
    #
    # print("huuu")

    # r = requests.post('http://127.0.0.1:8089/add_post', json={"user_id":"1bf48208-69f5-11ea-a502-28e347aeb22f",
    #                                                           "room_id":"9fc0dd64-6a04-11ea-b2d4-28e347aeb22f",
    #                                                           "content":"HelloWorld"})
    # print(r.status_code)
    # print(r.json())

    pass
