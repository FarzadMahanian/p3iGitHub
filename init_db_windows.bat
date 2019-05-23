SET FLASK_CONFIG=development
SET FLASK_APP=run.py

flask db init
flask db migrate
flask db upgrade