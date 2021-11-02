#!/bin/bash

#script to intilize SQLite3 database
#note: script also drop database cmd(flask drop_db), remove it if not required 
source env/bin/activate
export FLASK_APP=../src
export FLASK_ENV=development
flask drop_db
flask init_db
