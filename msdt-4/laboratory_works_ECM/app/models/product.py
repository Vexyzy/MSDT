from ..extensions import DB

class Product(DB.Model):
    __tablename__ = 'product'
    product_id = DB.Column(DB.Integer, primary_key=True)
    product_name = DB.Column(DB.String(300), nullable=False)
    brand_id = DB.Column(DB.ForeignKey("brand.brand_id"), nullable=True)
    measurement = DB.Column(DB.String(50), nullable=False)
    price = DB.Column(DB.Integer, nullable=False)
