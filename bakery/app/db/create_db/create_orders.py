# create orders

import sqlite3
import sys
import random

db_file = sys.argv[1]

conn = sqlite3.connect(db_file)

cur = conn.cursor()

EmployeeIDs = []
for val in cur.execute("SELECT EmployeeID FROM Employee").fetchall():
	EmployeeIDs.append(val[0])

productIDs = []
for val in cur.execute("SELECT ProductID, Price FROM Product").fetchall():
	productIDs.append(val)

customerIDs = []
for val in cur.execute("SELECT CustomerID FROM Customer").fetchall():
	customerIDs.append(val[0])

OrderProducts_count = 0
for i in range(1, 12000):

	price = 0

	prods = random.sample(list(enumerate(productIDs)), 5)
	for j in range(1, random.randint(2, 5)):
		query = "INSERT INTO OrderProducts VALUES (?, ?)"
		query_args = (i, prods[j][1][0])
		price += prods[j][1][1]
		cur.execute(query, query_args)
		OrderProducts_count += 1

	query = "INSERT INTO CustomerOrders VALUES (?, ?)"
	query_args = (i, random.choice(customerIDs))
	cur.execute(query, query_args)


	query = "INSERT INTO _Order VALUES (?, ?, ?, ?, ?)"
	query_args = (i, price, random.randint(946684800, 1483228800), 1, random.choice(EmployeeIDs))
	cur.execute(query, query_args)

conn.commit()

print("Added %i values to _Order" % i)
print("Added %i values to CustomerOrders" % i)
print("Added %i values to OrderProducts" % OrderProducts_count)


