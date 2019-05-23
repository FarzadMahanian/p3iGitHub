# instance/config.py
import os
SECRET_KEY = 'p3i_information_systems'
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.getcwd() + '/p3i.db'
