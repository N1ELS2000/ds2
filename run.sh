#! /bin/bash
docker compose down
docker compose down --volumnes
docker volume rm ds2_songs_data
docker volume rm ds2_user_data
docker volume rm ds2_friends_data
docker compose up --build