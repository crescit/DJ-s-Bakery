-- Create Schema

CREATE TABLE Ingredient (
	IngredientID INT PRIMARY KEY,
	Name CHAR(50),
	SupplierID INT NOT NULL,
	FOREIGN KEY (SupplierID) REFERENCES Supplier(SupplierID)
);

CREATE TABLE Supplier (
	SupplierID INT PRIMARY KEY,
	Name CHAR(50)
);

CREATE TABLE RecipeIngredients (
	RecipeID INT,
	IngredientID INT,
	PRIMARY KEY (RecipeID, IngredientID)
	FOREIGN KEY (IngredientID) REFERENCES Ingredient(IngredientID)
);

CREATE TABLE Recipe (
	RecipeID INT PRIMARY KEY,
	ProductID INT,
	Title CHAR(50),
	Text CHAR(1000), 
	IsActive BOOLEAN,
	FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

CREATE TABLE Category (
	CategoryID INT PRIMARY KEY,
	CatName CHAR(50)
);

CREATE TABLE ProductCategories (
	ProductID INT,
	CategoryID INT,
	FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID), 
	FOREIGN KEY (ProductID) REFERENCES Product(ProductID),
	PRIMARY KEY (ProductID, CategoryID)
);

CREATE TABLE Product (
	ProductID INT PRIMARY KEY,
	Name CHAR(50), 
	Price DECIMAL(6, 2)
);

CREATE TABLE EmployeeRoles (
	EmployeeID INT,
	RoleID INT,
	PRIMARY KEY (EmployeeID, RoleID), 
	FOREIGN KEY (RoleID) REFERENCES Role(RoleID)
);

CREATE TABLE Role (
	RoleID INT PRIMARY KEY,
	Name CHAR(50)
);

CREATE TABLE Employee (
	EmployeeID INT PRIMARY KEY,
	Name Char(50),
	SSN CHAR(9),
	Password CHAR(30)
);

CREATE TABLE _Order (
	OrderID INT PRIMARY KEY,
	TotalSum DECIMAL(6, 2),
	Created DATETIME,
	IsClosed BOOLEAN,
	PerformedBy INT,
	FOREIGN KEY (PerformedBy) REFERENCES Employee(EmployeeID)
);

CREATE TABLE OrderProducts (
	OrderID INT,
	ProductID INT,
	PRIMARY KEY (OrderID, ProductID)
	FOREIGN KEY (orderID) REFERENCES _Order(OrderID),
	FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);

CREATE TABLE CustomerOrders (
	OrderID INT PRIMARY KEY,
	CustomerID INT,
	FOREIGN KEY (OrderID) REFERENCES _Order(OrderID),
	FOREIGN KEY (CustomerID) REFERENCES Customer(email)
);

CREATE TABLE Customer (
	CustomerID CHAR(100) PRIMARY KEY,
	Name CHAR(50),
	BirthDate DATE,
	Password CHAR(30)
);


