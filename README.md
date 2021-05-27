# kinexcstask
To implement an API server with several features

**Database entries**


Entity name - **customer** 

Attributes - id, name, dob

Entity name - **order**

Attributes - item name, item price, date time and customer id as foreign key


**End points**


/customer -> Get all customer objects and return as json

/order -> Get all orders and return as json

/order?customer_id=x -> Get all the order for customer x, where x is the customer id

/customer?number=n -> Get n youngest customers

/customer/create -> Create a customer
