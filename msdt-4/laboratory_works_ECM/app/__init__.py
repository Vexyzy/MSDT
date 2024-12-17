from flask import Flask

from .etc.logger import logger
from .etc.config import Config
from .extensions import DB, MIGRATE
from .routes.brand import BRAND
from .routes.cosmetic_order import ORDER
from .routes.delivery import DELIVERY
from .routes.enterprise import ENTERPRISE
from .routes.error import ERROR
from .routes.product import PRODUCT
from .routes.report import REPORT

@logger.catch
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(ERROR)
    app.register_blueprint(BRAND)
    app.register_blueprint(PRODUCT)
    app.register_blueprint(ORDER)
    app.register_blueprint(ENTERPRISE)
    app.register_blueprint(DELIVERY)
    app.register_blueprint(REPORT)

    DB.init_app(app)
    MIGRATE.init_app(app, DB)

    with app.app_context():
        DB.create_all()

    return app
