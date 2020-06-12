# The purpose of this file is pure exploritory. To play with the data, clean it up, and populate 
# additional information if need be. 

from datetime import timedelta, datetime
from random import randint
from random import choice as rc
import sqlite3

# The first function will return a random datetime between to dt objects.
def random_date(start, end):
    return start + timedelta(seconds=randint(0, int((end - start).total_seconds())))

# Next I will start by connecting to the db.
conn = sqlite3.connect('Northwind.sqlite')
c = conn.cursor

# Next I will select ShipName, Address, City, Region and PostalCode
c.execute("SELECT DISTINCT ShipName, ShipAddress, ShipCity, ShipRegion, ShipPostalCode, ShipCountry from [Order]")
locations = [(row[0], row[1], row[2], row[3], row[4], row[5]) for row in c.fetchall()]

# Need to execute Customer.Id from Employee
c.execute("SELECT DISTINCT Id FROM [Employee]")
employees = [row[0] for row in c.fetchall()]

# Need to execute Shipper.Id
c.execute("SELECT DISTINCT Id FROM [Shipper]")
shippers = [row[0] for row in c.fetchall()]

# Need to execute Customer Id from Customer
c.execute("SELECT DISTINCT Id FROM [Customer]")
customers = [row[0] for row in c.fetchall()]

# Next I will create new orders
for i in range(randint(15000, 16000)):
    sql = 'INSERT INTO [Order] (CustomerId, EmployeeId, OrderDate, RequiredDate, ShippedDate, ShipVia, Freight, ShipName, ShipAddress, ShipCity, ShipRegion, ShipPostalCode, ShipCountry) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    location = rc(locations)
    order_date = random_date(datetime.strptime('2012-07-10', '%Y-%m-%d'), datetime.today())
    required_date =  random_date(order_date, order_date+timedelta(days=randint(14,60)))
    shipped_date = random_date(order_date, order_date+timedelta(days=randint(1,30)))
    params = (
      rc(customers),   # This equals CustomerId
      rc(employees),   # Employee Id
      order_date,      # Order Date
      required_date,   # Required Date
      shipped_date,    # Shipped Date
      rc(shippers),    # How it is Shipped
      0.00,            # Freight
      location[0],     # Ship Name
      location[1],     # Address
      location[2],     # City
      location[3],     # Region
      location[4],     # Postal Code
      location[5],     # Country
    )
    c.execute(sql, params)

# Now I need to execute Product.Id
c.execute("SELECT DISTINCT Id, UnitPrice FROM [Product]")
products = [(row[0], row[1]) for row in c.fetchall()]

# Next up is OrderId
c.execute("SELECT DISTINCT Id FROM [Order] WHERE Freight = 0.00")
orders = [row[0] for row in c.fetchall()]

# This should fill the order with items
for order in orders:
    used = []
    for x in range(randint(1, len(products))):
        sql = 'INSERT INTO [OrderDetail] (Id, OrderId, ProductId, UnitPrice, Quantity, Discount) VALUES (?, ?, ?, ?, ?, ?)'
        control = 1
        while control:
            product = rc(products)
            if product not in used:
                used.append(product)
                control = 0
        params = (
            "%s/%s" % (order, product[0]),
            order,       # OrderId
            product[0],  # ProductId
            products[1], # Unit Price
            randint(1, 50), # Quantity
            0,           # Discount
            )
        c.execute(sql, params)

# Time for cleanup
c.execute("SELECT sum(Quantity)*0.25+10, OrderId FROM [OrderDetail] GROUP BY OrderId")
orders = [(row[0],row[1]) for row in c.fetchall()]
for order in orders:
    c.execute("update [Order] set Freight=? where Id=?", (order[0], order[1]))

conn.commit()
conn.close()