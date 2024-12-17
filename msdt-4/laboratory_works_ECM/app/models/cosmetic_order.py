from ..extensions import DB

class CosmeticOrder(DB.Model):
    __tablename__ = 'cosmetic_order'

    cosmetic_order_id = DB.Column(
        DB.BigInteger,
        primary_key=True
    )

    enterprise_id = DB.Column(
        DB.ForeignKey('enterprise.enterprise_id'),
        nullable=False
    )

    product_id = DB.Column(
        DB.ForeignKey('product.product_id'),
        nullable=False
    )

    quantity_of_product = DB.Column(DB.Integer, nullable=False)
    order_date = DB.Column(DB.DateTime, nullable=False)
    execution_date = DB.Column(DB.DateTime, nullable=False)