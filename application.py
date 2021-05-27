from flask import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost/postgres'

app.config['DEBUG'] = True

db = SQLAlchemy(app)

class customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    dob = db.Column(db.Date(), nullable = False)

    def __init__(self, name, dob):
        self.name = name
        self.dob = dob

class order(db.Model):
    __tablename__ = 'order'
    item_name = db.Column(db.String(200), nullable = False)
    item_price = db.Column(db.Integer, nullable = False)
    datetime = db.Column(db.DateTime(), primary_key = True, nullable = False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key = True)

    def __init__(self, item_name, item_price, datetime, customer_id):
        self.item_name = item_name
        self.item_price = item_price
        self.datetime = datetime
        self.customer_id = customer_id

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/customer')
def getCustomers():
    output = []
    args = request.args
    if "number" in args:
        num_youngest = int(args.get("number"))
        youngest_cust = customer.query.order_by(customer.dob.desc()).limit(num_youngest).all()
        for customers in youngest_cust:
            customerList = {}
            customerList['id'] = customers.id
            customerList['name'] = customers.name
            customerList['dob'] = customers.dob
            output.append(customerList)

    else:
        allCustomers = customer.query.all()
        for customers in allCustomers:
            customerList = {}
            customerList['id'] = customers.id
            customerList['name'] = customers.name
            customerList['dob'] = customers.dob
            output.append(customerList)

    return jsonify(output)

@app.route('/order')
def getOrders():
    allOrders = order.query.all()
    output = []
    args = request.args
    if "customer_id" in args:
        cust_id = int(args.get("customer_id"))
        for orders in allOrders:
            orderList = {}
            orderList['item_name'] = orders.item_name
            orderList['item_price'] = orders.item_price
            orderList['datetime'] = orders.datetime
            if (orders.customer_id == cust_id):
                output.append(orderList)
    else:
        for orders in allOrders:
            orderList = {}
            orderList['item_name'] = orders.item_name
            orderList['item_price'] = orders.item_price
            orderList['datetime'] = orders.datetime
            orderList['customer_id'] = orders.customer_id
            output.append(orderList)

    return jsonify(output)

@app.route('/customer/create')
def createCustomer():
    return render_template('createCustomer.html')

@app.route('/submit', methods = ['POST'])
def created():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        data = customer(name, dob)
        db.session.add(data)
        db.session.commit()
        if name == '' or dob == '':
            return render_template('createCustomer.html', message='Enter required fields.')
        return render_template('createdpage.html')

if __name__ == '__main__':
    app.run()