from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

DB = SQLAlchemy()
MIGRATE = Migrate()
UPLOAD_FOLDER = 'excel/uploads'
ALLOWED_EXTENSIONS = {'xlsx'}
