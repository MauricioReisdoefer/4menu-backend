from db import db

class FavoriteRestaurantModel(db.Model):
    __tablename__ = "restaurants"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    
    owner = db.relationship("UserModel", back_populates="restaurants")