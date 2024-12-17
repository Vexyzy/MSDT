from ..extensions import DB

class Brand(DB.Model):
    brand_id = DB.Column(DB.Integer, primary_key=True)
    brand_name = DB.Column(DB.String(150), nullable=False)