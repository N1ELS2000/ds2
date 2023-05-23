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
    if check_playlist(user, title):
        cur = conn.cursor()
        cur.execute("INSERT INTO playlists (title, owner) VALUES (\'{}\', \'{}\');".format(title, user))
        r = conn.commit()
        print("Inside add_playlist ", str(r), flush=True)
        return True
    return False


def check_playlist(user, title):
    cur = conn.cursor()
    cur.execute("SELECT * FROM playlists WHERE title = \'{}\' AND owner = \'{}\';".format(title, user))
    t = cur.fetchone()
    print("inside check_playlist: ", str(t), flush=True)
    if t is not None:
        return False
    return True


def get_own_playlists(owner):
    cur = conn.cursor()
    cur.execute("SELECT id, title FROM playlists WHERE owner = \'{}\';".format(owner))
    t = cur.fetchall()
    print("Inside get_own_playlists, the answer for owner: ", owner, " is: ", str(t), flush=True)
    return t


class AddPlaylist(Resource):
    def put(self):
        args = flask_request.args
        return add_playlist(args['username'], args['title'])


class GetOwnPlaylists(Resource):
    def get(self):
        args = flask_request.args
        return get_own_playlists(args['username'])


api.add_resource(AddPlaylist, '/playlists/add/')
api.add_resource(GetOwnPlaylists, '/playlists/own/')
