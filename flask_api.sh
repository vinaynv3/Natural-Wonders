#!/bin/bash

source env/bin/activate

export FLASK_APP=src
export FLASK_ENV=development
echo $FLASK_APP
flask shell


