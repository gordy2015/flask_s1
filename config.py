
from flask import Flask
import os,sqlite3
from flask_sqlalchemy import SQLAlchemy

Flask.debug = True

Flask.reload = True
DATABASE = 'db.sqlite'

# basedir = os.path.abspath(os.path.dirname(__file__))
# SQLALCHEMY_DATABASE_URI = 'sqilte://' + os.path.join(basedir, DATABASE)
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False


