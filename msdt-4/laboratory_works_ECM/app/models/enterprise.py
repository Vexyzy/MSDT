from ..extensions import DB

class Enterprise(DB.Model):
    __tablename__ = 'enterprise'
    enterprise_id = DB.Column(DB.Integer, primary_key=True)
    enterprise_name = DB.Column(DB.String(300), nullable=False)
    address = DB.Column(DB.String(400), nullable=False)
    phone= DB.Column(DB.String(16))

