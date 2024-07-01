from flask import Flask, jsonify, request
from flask_cors import CORS 

# Flask - gives us all the tools we need to run a flask app by creating an instance of this class
# jsonify - converst data to JSON
# request - allows us to interact with HTTP method requests as objects
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy = ORM to connect and relate python classes to SQL tables
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# DeclarativeBase - gives ust the base model functionallity to create the Classes as Model Classes for our db tables
# Mapped - Maps a Class attribute to a table column or relationship
# mapped_column - sets our Column and allows us to add any constraints we need (unique,nullable, primary_key)
from flask_marshmallow import Marshmallow

# Marshmallow - allows us to create a schema to valdite, serialize, and deserialize JSON data
from datetime import date

# date - use to create date type objects
from typing import List

# List - is used to creat a relationship that will return a list of Objects
from marshmallow import ValidationError, fields

# fields - lets us set a schema field which includes datatype and constraints
from sqlalchemy import select, delete

# select - acts as our SELECT FROM query
# delete - acts as our DELET query


app = Flask(__name__)  # creating and instance of our flask app
CORS(app)
# user pw     host      db
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:@localhost/ecomm_db"


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(app, model_class=Base)
ma = Marshmallow(app)


class Customer(Base):
    __tablename__ = "Customer"  # Make your class name the same as your table name (trust me)

    # mapping class attributes to database table columns
    id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column(db.String(200), nullable=False)
    email: Mapped[str] = mapped_column(db.String(300))
    phone: Mapped[str] = mapped_column(db.String(16))
    # creating one-to-many relationship to Orders table
    orders: Mapped[List["Orders"]] = db.relationship(back_populates="customer")  # back_populates insures that both ends of the relationship have access to the other


order_products = db.Table(
    "Order_Products",
    Base.metadata,  # Allows this table to locate the foreign keys from the other Base class
    db.Column("order_id", db.ForeignKey("Orders.id"), primary_key=True),
    db.Column("product_id", db.ForeignKey("Products.id"), primary_key=True),
)

# order_status_check = db.Table(
#     "Orders_Status_Check",
#     Base.metadata,  # Allows this table to locate the foreign keys from the other Base class
#     db.Column("order_id", db.ForeignKey("Orders.id"), primary_key=True),
#     db.Column("order_status_id", db.ForeignKey("Order_Status.id"), primary_key=True))


class Orders(Base):
    __tablename__ = "Orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_date: Mapped[date] = mapped_column(db.Date, nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey("Customer.id"))
    # creating a many-to-one relationship to Customer table
    customer: Mapped["Customer"] = db.relationship(back_populates="orders")
    # creating a many-to-many relationship to Products through or association table order_products
    products: Mapped[List["Products"]] = db.relationship(secondary=order_products)
    # order_status: Mapped[List["OrderStatus"]] = db.relationship(secondary=order_status_check)



class Products(Base):
    __tablename__ = "Products"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)



class OrderStatus(Base):
    __tablename__ = "Order_Status"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(db.ForeignKey("Orders.id"))
    status: Mapped[str] = mapped_column(db.String(100), nullable=False)
    timestamp: Mapped[date] = mapped_column(db.Date, nullable=False, default=date)


# Initialize the database and create tables
with app.app_context():
    #    db.drop_all()
    db.create_all()  # First check which tables already exist, and then create and tables it couldn't find
    # However if it finds a table with the same name, it doesn't construct or modify


# ============================ CRUD OPERATIONS ==================================


# Defin Customer Schema
class CustomerSchema(ma.Schema):
    id = fields.Integer(required=False)
    customer_name = fields.String(required=True)
    email = fields.String(required=True)
    phone = fields.String(required=True)

    class Meta:
        fields = ("id", "customer_name", "email", "phone")


class ProductSchema(ma.Schema):
    id = fields.Integer(required=False)
    product_name = fields.String(required=True)
    price = fields.Float(required=True)

    class Meta:
        fields = ("id", "product_name", "price")


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)


@app.route("/")
def home():
    return "Welcome to the E-Commerce Database!"


# ====================Customer Interactions==========================


# Get all customers using a GET method
@app.route("/customers", methods=["GET"])
def get_customers():
    query = select(Customer)
    result = db.session.execute(query).scalars()  # Exectute query, and convert row objects into scalar objects (python useable)
    customers = result.all()  # packs objects into a list
    return customers_schema.jsonify(customers)


# Get Specific customer using GET method and dynamic route
@app.route("/customers/<int:id>", methods=["GET"])
def get_customer(id):

    query = select(Customer).filter(Customer.id == id)
    result = (db.session.execute(query).scalars().first())  # first() grabs the first object return

    if result is None:
        return jsonify({"Error": "Customer not found"}), 404

    return customer_schema.jsonify(result)


# Creating customers with POST request
@app.route("/customers", methods=["POST"])
def add_customer():

    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_customer = Customer(customer_name=customer_data["customer_name"], email=customer_data["email"], phone=customer_data["phone"])
    db.session.add(new_customer)
    db.session.commit()

    return jsonify({"Message": "New Customer added successfully"}), 201


# Update a user with PUT request
@app.route("/customers/<int:id>", methods=["PUT"])
def update_customer(id):

    query = select(Customer).where(Customer.id == id)
    result = db.session.execute(query).scalars().first()
    if result is None:
        return jsonify({"Error": "Customer not found"}), 404

    customer = result

    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for field, value in customer_data.items():
        setattr(customer, field, value)

    db.session.commit()
    return jsonify({"Message": "Customer details have been updated!"})


# Delete a user with DELETE request
@app.route("/customers/<int:id>", methods=["DELETE"])
def delete_customer(id):
    query = delete(Customer).filter(Customer.id == id)

    result = db.session.execute(query)

    if result.rowcount == 0:
        return jsonify({"Error": "Customer not found"}), 404

    db.session.commit()
    return jsonify({"Message": "Customer removed Successfully!"}), 200


# ====================Products Interactions==========================


@app.route("/products", methods=["POST"])
def add_product():
    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_product = Products(product_name=product_data["product_name"], price=product_data["price"])
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"Messages": "New Product added!"}), 201


# Get Specific product using GET method and dynamic route
@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):

    query = select(Products).filter(Products.id == id)
    result = (db.session.execute(query).scalars().first())  # first() grabs the first object return

    if result is None:
        return jsonify({"Error": "Product not found"}), 404

    return product_schema.jsonify(result)


# Get all products using a GET method
@app.route("/products", methods=["GET"])
def get_products():
    query = select(Products)
    result = db.session.execute(
        query
    ).scalars()  # Exectute query, and convert row objects into scalar objects (python useable)
    products = result.all()  # packs objects into a list
    return products_schema.jsonify(products)


# Update a product with PUT request
@app.route("/products/<int:id>", methods=["PUT"])
def update_product(id):

    query = select(Products).where(Products.id == id)
    result = db.session.execute(query).scalars().first()
    if result is None:
        return jsonify({"Message": "Product not found"}), 404

    product = result

    try:
        product_data = product_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    for field, value in product_data.items():
        setattr(product, field, value)

    db.session.commit()
    return jsonify({"Message": "Product details have been updated!"})


# Delete a product with DELETE request
@app.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    query = delete(Products).filter(Products.id == id)

    result = db.session.execute(query)

    if result.rowcount == 0:
        return jsonify({"Error": "Product not found"}), 404

    db.session.commit()
    return jsonify({"Message": "Product removed Successfully!"}), 200


# ====================Order Operations================================


class OrderSchema(ma.Schema):
    id = fields.Integer(required=False)
    order_date = fields.Date(required=False)
    customer_id = fields.Integer(required=True)
    items = fields.List(fields.Integer())

    class Meta:
        fields = ("id", "order_date", "customer_id", "items")  # items will be a list of product_ids


order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


class OrderStatusSchema(ma.Schema):
    id = fields.Integer(required=False)
    order_id = fields.Integer(required=True)
    status = fields.String(required=True)
    timestamp = fields.Date(required=True)

    class Meta:
        fields = ("id", "order_id", "status", "timestamp")


order_status_schema = OrderStatusSchema()


@app.route("/orders", methods=["POST"])
def add_order():
    
    try:
        order_data = order_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_order = Orders(
        order_date=date.today(), customer_id=order_data["customer_id"]
    )

    for item_id in order_data["items"]:
        query = select(Products).filter(Products.id == item_id)
        item = db.session.execute(query).scalar()
        new_order.products.append(item)

    db.session.add(new_order)
    db.session.commit()

    return jsonify({"Message": "New Order Placed!"}), 201


@app.route("/order_items/<int:id>", methods=["GET"])
def order_items(id):
    query = select(Orders).filter(Orders.id == id)
    order = db.session.execute(query).scalar()
    return products_schema.jsonify(order.products)


@app.route("/order_status/<int:id>", methods=["GET"])

def order_status(id):
    # Retrieve the order with the given id
    query = select(Orders).filter(Orders.id == id)
    order = db.session.execute(query).scalar()
    print(order)
    if order is None:
        return jsonify({"Message": "Order not found"}), 404

    # Retrieve the status of the order
    query1 = select(OrderStatus).filter(Orders.id == id).order_by(OrderStatus.timestamp.desc())
   
    order_status = db.session.execute(query1).scalar()
    print(order_status)

    if order_status is None:
        return jsonify({"Message": "No status found for this order"}), 404

    order_status_data = order_status_schema.dump(order_status)
    return jsonify(order_status_data), 200


if __name__ == "__main__":
    app.run(debug=True)
