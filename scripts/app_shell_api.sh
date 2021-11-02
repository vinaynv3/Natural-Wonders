#!/bin/bash

#activate virtual environment
source ../env/bin/activate

# export flask app
export FLASK_APP=../src
export FLASK_ENV=development
echo $FLASK_APP
flask shell


