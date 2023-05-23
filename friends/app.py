from flask import Flask
from flask import request as flask_request
from flask_restful import Resource, Api, reqparse
import psycopg2

parser = reqparse.RequestParser()
parser.add_argument('id_one')
parser.add_argument('id_two')

app = Flask("friends")
api = Api(app)

conn = None

while conn is None:
    try:
        conn = psycopg2.connect(dbname="friends", user="postgres", password="postgres", host="friends_persistence")
        print("DB connection successful")
    except psycopg2.OperationalError:
        import time

        time.sleep(1)
        print("Retrying DB connection")


# this function checks if the tuple (id1, id2) is already in our database
def check_friends(id1, id2):
    cur = conn.cursor()
    cur.execute("SELECT * FROM friends WHERE id_one = {} AND id_two = {};".format(id1, id2))
    if cur.fetchone() is None:
        return False
    return True


def add_friends(id1, id2):
    # if the two ids are not yet in our database and therefor are not yet friends
    if not check_friends(id1, id2):
        # add them to the database
        cur = conn.cursor()
        cur.execute("INSERT INTO friends (id_one, id_two) VALUES ({}, {});".format(id1, id2))
        conn.commit()
        return True
    return False


def get_friends(id1):
    # select all tuples where id_one = id1
    cur = conn.cursor()
    cur.execute("SELECT id_two FROM friends WHERE id_one = {};".format(id1))
    t = cur.fetchall()
    print("Inside get_friends the returned answer is: ", str(t), flush=True)
    return t


class AddFriends(Resource):
    def put(self):
        args = flask_request.args
        return add_friends(args['id_one'], args['id_two'])


class GetFriends(Resource):
    def get(self):
        args = flask_request.args
        return get_friends(args['id_one'])


api.add_resource(AddFriends, '/friend/add/')
api.add_resource(GetFriends, '/friend/friends_of/')
