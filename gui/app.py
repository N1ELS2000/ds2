import sys

from flask import Flask, render_template, redirect, request, url_for
import requests

app = Flask(__name__)


# The Username & Password of the currently logged-in User
username = None
password = None

session_data = dict()


def save_to_session(key, value):
    session_data[key] = value


def load_from_session(key):
    return session_data.pop(key) if key in session_data else None  # Pop to ensure that it is only used once


@app.route("/")
def feed():
    # ================================
    # FEATURE 9 (feed)
    #
    # Get the feed of the last N activities of your friends.
    # ================================
    global username

    N = 10

    if username is not None:
        feed = []  # TODO: call
    else:
        feed = []

    return render_template('feed.html', username=username, password=password, feed=feed)


@app.route("/catalogue")
def catalogue():
    songs = requests.get("http://songs:5000/songs").json()

    return render_template('catalogue.html', username=username, password=password, songs=songs)


@app.route("/login")
def login_page():

    success = bool(load_from_session('success'))
    return render_template('login.html', username=username, password=password, success=success)


@app.route("/login", methods=['POST'])
def actual_login():
    req_username, req_password = request.form['username'], request.form['password']

    # ================================
    # FEATURE 2 (login)
    #
    # send the username and password to the microservice
    # microservice returns True if correct combination, False if otherwise.
    # Also pay attention to the status code returned by the microservice.
    # ================================
    success = requests.get("http://users:5000/user/login/", params={'username': req_username, 'password': req_password})

    save_to_session('success', success)
    if success:
        global username, password

        username = req_username
        password = req_password

    return redirect('/login')


@app.route("/register")
def register_page():
    success = bool(load_from_session('success'))
    return render_template('register.html', username=username, password=password, success=success)


@app.route("/register", methods=['POST'])
def actual_register():
    req_username, req_password = request.form['username'], request.form['password']

    # ================================
    # FEATURE 1 (register)
    #
    # send the username and password to the microservice.
    # microservice returns True if registration is successful, False if otherwise.
    #
    # Registration is successful if a user with the same username doesn't exist yet.
    # ================================
    # make the call
    test = requests.put("http://users:5000/user/add", params={'username': req_username, 'password': req_password})
    # add the boolean to the success variable
    success = test

    save_to_session('success', success)

    if success:
        global username, password

        username = req_username
        password = req_password

    return redirect('/register')


@app.route("/friends")
def friends():
    success = load_from_session('success')

    global username

    # ================================
    # FEATURE 4
    #
    # Get a list of friends for the currently logged-in user
    # ================================

    if username is not None:
        # first get the id of the currently logged-in user
        id_one = requests.get("http://users:5000/user/id/", params={'username': username}).json()
        # then get all the friends of this user
        all_friends = requests.get("http://friends:5000/friend/friends_of/", params={'id_one': id_one}).json()
        friend_list = []
        # now convert the list of ids all_friends to a list of usernames friend_list
        for a_id in all_friends:
            name = requests.get("http://users:5000/user/id_of/", params={'user_id': a_id}).json()
            friend_list.append(name)
    else:
        friend_list = []  # TODO: call

    return render_template('friends.html', username=username, password=password, success=success, friend_list=friend_list)


@app.route("/add_friend", methods=['POST'])
def add_friend():

    # ==============================
    # FEATURE 3
    #
    # send the username of the current user and the username of the added friend to the microservice.
    # microservice returns True if the friend request is successful (the friend exists & is not already friends),
    # False if otherwise
    # ==============================

    global username
    req_username = request.form['username']

    # first get the id's of the given users
    id_one = requests.get("http://users:5000/user/id/", params={'username': username}).json()
    print("Inside add_friend in GUI, id_one = ", id_one, flush=True)
    id_two = requests.get("http://users:5000/user/id/", params={'username': req_username}).json()
    print("And id_two = ", id_two, flush=True)

    # if id_two == -1 then the user does not exist, success is False
    if id_two == -1:
        success = False
    # else, we feed those id's to the friends microservice
    else:
        success = requests.put("http://friends:5000/friend/add/", params={'id_one': id_one, 'id_two': id_two})

    save_to_session('success', success)

    return redirect('/friends')


@app.route('/playlists')
def playlists():
    global username

    my_playlists = []
    shared_with_me = []

    if username is not None:
        # ================================
        # FEATURE
        #
        # Get all playlists you created and all playlist that are shared with you. (list of id, title pairs)
        # ================================

        my_playlists = []  # TODO: call
        shared_with_me = []  # TODO: call

    return render_template('playlists.html', username=username, password=password, my_playlists=my_playlists, shared_with_me=shared_with_me)


@app.route('/create_playlist', methods=['POST'])
def create_playlist():
    # ================================
    # FEATURE 5
    #
    # Create a playlist by sending the owner and the title to the microservice.
    # ================================
    global username
    title = request.form['title']

    # TODO: call

    return redirect('/playlists')


@app.route('/playlists/<int:playlist_id>')
def a_playlist(playlist_id):
    # ================================
    # FEATURE 7
    #
    # List all songs within a playlist
    # ================================
    songs = [] # TODO: call
    return render_template('a_playlist.html', username=username, password=password, songs=songs, playlist_id=playlist_id)


@app.route('/add_song_to/<int:playlist_id>', methods=["POST"])
def add_song_to_playlist(playlist_id):
    # ================================
    # FEATURE 6
    #
    # Add a song (represented by a title & artist) to a playlist (represented by an id)
    # ================================
    title, artist = request.form['title'], request.form['artist']

    # TODO: call
    return redirect(f'/playlists/{playlist_id}')


@app.route('/invite_user_to/<int:playlist_id>', methods=["POST"])
def invite_user_to_playlist(playlist_id):
    # ================================
    # FEATURE 8
    #
    # Share a playlist (represented by an id) with a user.
    # ================================
    recipient = request.form['user']

    # TODO: call
    return redirect(f'/playlists/{playlist_id}')


@app.route("/logout")
def logout():
    global username, password

    username = None
    password = None
    return redirect('/')
