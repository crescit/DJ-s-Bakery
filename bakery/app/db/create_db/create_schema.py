import sys
import random
import sqlite3


db_file = sys.argv[1]

conn = sqlite3.connect(db_file)

cur = conn.cursor()


query = '''
	CREATE TABLE Ingredient (
	IngredientID INT PRIMARY KEY,
	Name CHAR(50),
	SupplierID INT NOT NULL,
	FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
);'''
cur.execute(query)

query = '''
CREATE TABLE Supplier (
	SupplierID INT PRIMARY KEY,
	Name CHAR(50)
);'''
cur.execute(query)

query = '''
CREATE TABLE RecipeIngredients (
	RecipeID INT,
	IngredientID INT,
	PRIMARY KEY (RecipeID, IngredientID)
	FOREIGN KEY (IngredientID) REFERENCES Ingredient(IngredientID)
);'''
cur.execute(query)

query = '''
CREATE TABLE Recipe (
	RecipeID INT PRIMARY KEY,
	ProductID INT,
	Title CHAR(50),
	Text CHAR(1000), 
	IsActive BOOLEAN,
	FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);'''
cur.execute(query)

query = '''
CREATE TABLE Category (
	CategoryID INT PRIMARY KEY,
	CatName CHAR(50)
);'''
cur.execute(query)

query = '''
CREATE TABLE ProductCategories (
	ProductID INT,
	CategoryID INT,
	FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID), 
	FOREIGN KEY (ProductID) REFERENCES Product(ProductID),
	PRIMARY KEY (ProductID, CategoryID)
);'''
cur.execute(query)

query = '''
CREATE TABLE Product (
	ProductID INT PRIMARY KEY,
	Name CHAR(50), 
	Price DECIMAL(6, 2)
);'''
cur.execute(query)

query = '''
CREATE TABLE EmployeeRoles (
	EmployeeID INT,
	RoleID INT,
	PRIMARY KEY (EmployeeID, RoleID), 
	FOREIGN KEY (RoleID) REFERENCES Role(RoleID)
);'''
cur.execute(query)

query = '''
CREATE TABLE Role (
	RoleID INT PRIMARY KEY,
	Name CHAR(50)
);'''
cur.execute(query)

query = '''
CREATE TABLE Employee (
	EmployeeID INT PRIMARY KEY,
	Name Char(50),
	SSN CHAR(9),
	Password CHAR(30)
);'''
cur.execute(query)

query = '''
CREATE TABLE _Order (
	OrderID INT PRIMARY KEY,
	TotalSum DECIMAL(6, 2),
	Created DATETIME,
	IsClosed BOOLEAN,
	PerformedBy INT,
	FOREIGN KEY (PerformedBy) REFERENCES Employee(EmployeeID)
);'''
cur.execute(query)

query = '''
CREATE TABLE OrderProducts (
	OrderID INT,
	ProductID INT,
	PRIMARY KEY (OrderID, ProductID)
	FOREIGN KEY (orderID) REFERENCES _Order(OrderID),
	FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);'''
cur.execute(query)

query = '''
CREATE TABLE CustomerOrders (
	OrderID INT PRIMARY KEY,
	CustomerID INT,
	FOREIGN KEY (OrderID) REFERENCES _Order(OrderID),
	FOREIGN KEY (CustomerID) REFERENCES Customer(email)
);'''
cur.execute(query)

query = '''
CREATE TABLE Customer (
	CustomerID CHAR(100) PRIMARY KEY,
	Name CHAR(50),
	BirthDate DATE,
	Password CHAR(30)
);'''
cur.execute(query)


conn.commit()

