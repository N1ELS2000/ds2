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
    print("GOT HERE!")
    # first we need to check if the current username is already in the database or not
    if not (user_exists(username)):
        # add user to database by first selecting the latest used ID
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE CTID = (SELECT MAX(CTID) FROM users);")
        test = cur.fetchone()
        # if this is the first entry ever, user_id is 0
        if test is None:
            user_id = 0
        # else we add 1 to the latest user_id
        else:
            user_id = int(test["id"]) + 1
        # now we add to our database: the calculated id, the given username and the given password
        cur.execute("INSERT INTO user (id, username, password) VALUES (%s, %s, %s);", (user_id, username, password))
        cur.commit()
        return True
    return False


def user_exists(username):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM user (WHERE email = %s);", username)
    return bool(cur.fetchone()[0])  # Either True or False


class AddUser(Resource):
    def put(self):
        args = flask_request.args
        return add_user(args['username'], args['password'])


api.add_resource(AddUser, '/user/add/')
