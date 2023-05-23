#!/bin/bash

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE friends;

EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "friends" <<-EOSQL
    CREATE TABLE friends(
        id_one INTEGER NOT NULL,
        id_two INTEGER NOT NULL,
        PRIMARY KEY (id_one, id_two)
    );
EOSQL
