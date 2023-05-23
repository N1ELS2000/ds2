from flask import Flask
from flask import request as flask_request
from flask_restful import Resource, Api, reqparse
import psycopg2

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')

app = Flask("users")
api = Api(app)

conn = None

while conn is None:
    try:
        conn = psycopg2.connect(dbname="users", user="postgres", password="postgres", host="user_persistence")
        print("DB connection successful")
    except psycopg2.OperationalError:
        import time

        time.sleep(1)
        print("Retrying DB connection")


def add_user(username, password):
    # first we need to check if the current username is already in the database or not
    if not (user_exists(username)):
        # add user to database by first selecting the latest used ID
        cur = conn.cursor()
        # now we add to our database: the calculated id, the given username and the given password
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s);", (username, password))
        conn.commit()
        return True
    return False


def user_exists(username):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users  WHERE username = \'{}\';".format(username))
    if cur.fetchone() is None:
        return False
    return True


def check_user(username, password):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = \'{}\' AND password = \'{}\';".format(username, password))
    if cur.fetchone() is None:
        return False
    return True


class AddUser(Resource):
    def put(self):
        args = flask_request.args
        return add_user(args['username'], args['password'])


class CheckUser(Resource):
    def get(self):
        args = flask_request.args
        return check_user(args['username'], args['password'])


api.add_resource(AddUser, '/user/add/')
api.add_resource(CheckUser, '/user/login/')
