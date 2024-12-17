from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from loguru import logger

DB = SQLAlchemy()
MIGRATE = Migrate()
UPLOAD_FOLDER = 'excel/uploads'
ALLOWED_EXTENSIONS = {'xlsx'}
