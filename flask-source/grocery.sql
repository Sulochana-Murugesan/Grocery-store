
CREATE TABLE Admin (
    Admin_ID INT NOT NULL,
    Admin_Name VARCHAR(25) NOT NULL,
    Password varchar(15) Not null,
    Contact_Number int Not null
);
INSERT INTO "Admin" VALUES(901,'Admin','Admin1@tcs',9638520741);
INSERT INTO "Admin" VALUES(902,'Admin2','Admin2@tcs',8520963741);
INSERT INTO "Admin" VALUES(903,'Admin3','Admin3@tcs',7410852963);
CREATE TABLE "Cart"(Product_ID int Not null,
	Product_Name varchar(15) Not null,Description varchar(20) Not null,Quantity int Not null,Price int Not null,Customer_id int Not null);
INSERT INTO "Cart" VALUES(101,'Apple','fruits',1,76,31216);
INSERT INTO "Cart" VALUES(103,'Banana','fruits',1,40,31216);
CREATE TABLE Orders(
	Order_ID int Not null,
	Order_Date Date Not null,
    Amount int Not null,
	Customer_ID int Not null,
	Payment_mode varchar Not null
	);
CREATE TABLE Products(Product_ID int Not null Primary Key,
	Product_Name varchar(15) Not null,Description varchar(20) Not null,Quantity int Not null,Price int Not null);
INSERT INTO "Products" VALUES(101,'Apple','Fruits',10,76);
INSERT INTO "Products" VALUES(102,'Grapes','Fruits',10,60);
INSERT INTO "Products" VALUES(103,'Banana','Fruits',30,40);
INSERT INTO "Products" VALUES(104,'Strawberry','Fruits',50,80);
INSERT INTO "Products" VALUES(105,'Orange','Fruits',20,90);
INSERT INTO "Products" VALUES(201,'Onion','Vegetables',25,30);
INSERT INTO "Products" VALUES(202,'Tomato','Vegetables',25,30);
INSERT INTO "Products" VALUES(203,'Potato','Vegetables',20,60);
INSERT INTO "Products" VALUES(204,'Carrot','Vegetables',20,80);
INSERT INTO "Products" VALUES(205,'Cauliflower','Vegetables',30,30);
INSERT INTO "Products" VALUES(301,'Lays','Snacks',50,30);
INSERT INTO "Products" VALUES(302,'Bingo','Snacks',30,30);
INSERT INTO "Products" VALUES(303,'Popcorn','Snacks',30,35);
INSERT INTO "Products" VALUES(304,'Potato Chips','Snacks',20,30);
INSERT INTO "Products" VALUES(305,'Mixture','Snacks',20,40);
INSERT INTO "Products" VALUES(401,'Wheat Flour','Staples',30,40);
INSERT INTO "Products" VALUES(402,'Sunflower Oil','Staples',15,100);
INSERT INTO "Products" VALUES(403,'Rice','Staples',20,60);
INSERT INTO "Products" VALUES(404,'Ghee','Staples',15,200);
INSERT INTO "Products" VALUES(405,'Butter','Staples',15,150);
INSERT INTO "Products" VALUES(501,'Chicken','Meat',10,250);
INSERT INTO "Products" VALUES(502,'Mutton','Meat',10,850);
INSERT INTO "Products" VALUES(503,'Fish','Meat',10,300);
INSERT INTO "Products" VALUES(504,'Prawns','Meat',10,300);
INSERT INTO "Products" VALUES(505,'Egg','Meat',100,7);
CREATE TABLE "Registration"(
	Customer_Name varchar(30) Not null,
	Email varchar(100) Not null,
    Password varchar(15) Not null,
	Address varchar(50) Not null,
 	Contact_Number int Not null,
    Customer_id int Not null,Status);
INSERT INTO "Registration" VALUES('Santhosh','santhoshmurugesan@tcs.com','Sandy@2024','Ammanpalayam, Erode',6374569200,53689,'Active');
INSERT INTO "Registration" VALUES('Vikram','vikram@tcs.com','Vinu@2024','Coimbatore',9791334700,31216,'Active');
INSERT INTO "Registration" VALUES('Kokil','kokilraj@tcs.com','Kokil@2024','Ambattur, Chennai',9566210044,39254,'Active');
INSERT INTO "Registration" VALUES('Harshith','harshith@tcs.com','Harsh@2024','Chennai',9551458427,86292,'Active');
INSERT INTO "Registration" VALUES('Nithya','nithya@tcs.com','Nithya@2024','Kanchipuram',7601995908,95648,'Active');
INSERT INTO "Registration" VALUES('Santhosh','sam123@tcs.com','Iam1@good','Chennai',1234567890,721768,'Active');
CREATE TABLE Wishlist(Product_ID int Not null Primary Key,
	Product_Name varchar(15) Not null,Description varchar(20) Not null,Quantity int Not null,Price int Not null,Customer_id int Not null);
COMMIT;
