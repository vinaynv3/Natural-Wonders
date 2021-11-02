#!/bin/bash
#starts development server
#note: if server fails or see any errors, verify flask app name

source ../env/bin/activate
export FLASK_APP=../src
export FLASK_ENV=development
flask run
