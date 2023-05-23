from flask import Flask
from flask import request as flask_request
from flask_restful import Resource, Api, reqparse
import psycopg2

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('play_id')
parser.add_argument('title')

app = Flask("playlists")
api = Api(app)

conn = None

while conn is None:
    try:
        conn = psycopg2.connect(dbname="playlists", user="postgres", password="postgres", host="playlists_persistence")
        print("DB connection successful")
    except psycopg2.OperationalError:
        import time

        time.sleep(1)
        print("Retrying DB connection")


def add_playlist(user, title):
    if not check_playlist(user, title):
        cur = conn.cursor()
        cur.execute("INSERT INTO playlists (title, owner) VALUES (\'{}\', \'{}\');".format(title, user))
        conn.commit()
        return True
    return False


def check_playlist(user, title):
    cur = conn.cursor()
    cur.execute("SELECT * FROM playlists WHERE title = \'{}\' AND owner = \'{}\';".format(title, user))
    t = cur.fetchone()
    if t is not None:
        return False
    return True


class AddPlaylist(Resource):
    def put(self):
        args = flask_request.args
        return add_playlist(args['username'], args['title'])


api.add_resource(AddPlaylist, '/playlists/add/')
