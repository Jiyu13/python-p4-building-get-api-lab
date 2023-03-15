from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Bakery(db.Model, SerializerMixin):
    __tablename__ = "bakeries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # 1-m relationship between bakery and baked_goods => baked_goods.bakery
    baked_goods = db.relationship("BakedGood", backref="bakery")
    serialize_rules = ('-baked_goods.bakery',)

    def __repr__(self):
        return f"""<Bakery {self.id}: {self.name}"""


class BakedGood(db.Model, SerializerMixin):
    __tablename__ = "baked_goods"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    bakery_id = db.Column(db.Integer, db.ForeignKey("bakeries.id"))
    serialize_rules = ('-bakery.baked_goods',)

    def __repr__(self):
        return f"""<BakedGood {self.id}: {self.name}, price: {self.price}"""