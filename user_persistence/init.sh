#!/bin/bash

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE users;

EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "users" <<-EOSQL
    CREATE TABLE user(
        id INTEGER NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        PRIMARY KEY (id)
    );
EOSQL
