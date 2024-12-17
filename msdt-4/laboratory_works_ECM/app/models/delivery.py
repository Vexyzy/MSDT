from ..extensions import DB

class Delivery(DB.Model):
    __tablename__ = 'delivery'
    delivery_id = DB.Column(DB.BigInteger, primary_key=True)
    cosmetic_order_id = DB.Column(
        DB.ForeignKey('cosmetic_order.cosmetic_order_id'), nullable=False
    )
    quantity_of_product = DB.Column(DB.Integer, nullable=False)
    execution_date = DB.Column(DB.DateTime)

