source env/bin/activate
export FLASK_APP=src
export FLASK_ENV=development
flask drop_db
flask init_db
