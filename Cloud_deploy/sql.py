import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
import random
import re
import copy
from tabulate import tabulate
from datetime import date
import sqlite3

con = sqlite3.connect('test.db')
customer = con.cursor()
customer.execute('''Create Table if not exists Registration(
	Customer_Name varchar(30) Not null,
	Email varchar(30) Not null,
    Password varchar(15) Not null,
	Address varchar(50) Not null,
 	Contact_Number int Not null,
    Customer_id int Not null,Status)''')
customer.execute('''Create Table if not exists Products(Product_ID int Not null Primary Key,
	Product_Name varchar(15) Not null,Description varchar(20) Not null,Quantity int Not null,Price int Not null ,
	Foreign key(Customer_ID) references Registration(Customer_ID))''')

customer.execute('''Create Table if not exists Cart(Product_ID int Not null Primary Key,
	Product_Name varchar(15) Not null,Description varchar(20) Not null,Quantity int Not null,Price int Not null,Customer_id int Not null)''')

customer.execute('''Create Table if not exists Wishlist(Product_ID int Not null Primary Key,
	Product_Name varchar(15) Not null,Description varchar(20) Not null,Quantity int Not null,Price int Not null,Customer_id int Not null)''')

customer.execute('''Create Table if not exists Orders(
	Order_ID int Not null,
	Order_Date Date Not null,
    Amount int Not null,
	Customer_ID int Not null);''')
con.commit()


class Product:
    def __init__(self, ID, name, desc, quan, price):
        self.ID = ID
        self.name = name
        self.desc = desc
        self.quan = quan
        self.price = price


class Customer:
    def __init__(self, name, email, password, address, contact_no, customer_id):
        self.name = name
        self.email = email
        self.password = password
        self.address = address
        self.contact_no = contact_no
        self.customer_id = customer_id
        self.status = "Active"


class Admin:
    def __init__(self, name, password, id):
        self.name = name
        self.password = password
        self.id = id


class OrderDetails:
    def __init__(self, tranid, orddate, ordamount, custid):
        self.orderid = tranid
        self.date = orddate
        self.amount = ordamount
        self.custid = custid


def newregister():
    flag = True
    # Name
    while flag:
        name = input("Name : ")
        r = 0
        case = 0
        for i in range(len(name)):
            if (ord(name[i]) > 32 and ord(name[i]) < 65):
                case = 1

        if (len(name) > 50):
            inp = "Name should be less than 50 letters"
            print_box(inp)
        else:
            r = 1
        if (case == 1):
            inp = "Name should not contain any Special characters or Numeric Values"
            print_box(inp)
            r = 0
        if (r == 1):
            break
    # email
    n = 1
    while (n == 1):
        email = input("email: ")
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z.-]+\.\b'
        j = re.match(pattern, email)
        if (j):
            condition = f"Email='{email}'"
            customer.execute(f'''select * from Registration where {condition}''')
            r = customer.fetchall()
            if (r == []):
                n = 0
            else:
                inp = "email Id already exists Kindly Change the email"
                print_box(inp)

            # for x in customerlist:
            #   if (email == x.email):
            #      inp = "email Id already exists Kindly Change the email"
            #     print_box(inp)
            #    r = 1
            # if (r == 0):
            #   n = 0
        else:

            inp = "Invalid Credentials Email should be in this format(example@anything.com)"
            print_box(inp)

    # password
    while flag:
        password = input("Password : ")
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%*&?^])[A-Za-z\d!@#$%^&*?]{8,12}$'
        if (re.match(pattern, password)):
            break

        else:
            inp = "Password should be 8-12 letters with one from each \n     1 Upper case \n     2 Lower case \n     3 Special Character \n     4 Numeric Value\n"
            print_box(inp)

    # address
    while flag:
        address = input("address : ")
        if (len(address) > 100):
            inp = "Address must be less than 100 letters"
            print_box(inp)
        if (address):
            break
        else:
            inp = "Address CannotBe Blank"
            print_box(inp)

    # contact Number
    while flag:
        contact_no = int(input("Contact number : "))
        if (len(str(contact_no)) != 10):
            inp = "Contact Number must be 10 digits"
            print_box(inp)
        else:
            break
    # customer z
    c_id = int(random.randint(10000, 99999))
    customer.execute('''Insert Into Registration(
	Customer_Name,Email,Password,Address,Contact_Number,
    Customer_ID,Status) values(?, ?, ?, ?, ?, ?, ?)''', (name, email, password, address, contact_no, c_id, 'Active'))
    con.commit()
    p = Customer(name, email, password, address, contact_no, c_id)
    inp = f"Customer Registration is successful for {p.customer_id}"
    print_box(inp)
    customer.execute('''select * from Registration''')
    r = customer.fetchall()
    table_data = [["name", "email", "password", "address", "contact_no", "c_id", "Status"]]
    for row in r:
        table_data.append(list(row))
    print(tabulate(table_data, headers="firstrow", tablefmt="fancy_grid"))

    return p


def updateCustomerDetails(customerlist, idval, cho, updatede):
    retur = False
    condition = f"Customer_ID='{idval}'"
    customer.execute(f'''select * from Registration where {condition}''')
    r = customer.fetchall()
    if (r != []):
        retur = True
        if cho == 1:
            case = 0
            for i in range(len(updatede)):
                if (ord(updatede[i]) > 32 and ord(updatede[i]) < 65):
                    case = 1
                    break

            if (case == 1):
                inp = "Name should not contain any Special characters or Numeric Values"
                print_box(inp)
                retur = False
            else:
                if (len(updatede) < 50):
                    condition = f"Customer_ID='{idval}'"
                    customer.execute(f'''Update Registration SET Customer_Name='{updatede}' where {condition}''')
                    con.commit()
                    retur = True
                else:
                    inp = "Name should be less than 50 letters"
                    print_box(inp)


        elif cho == 2:
            r = updatede
            pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z.-]+\.\b'
            j = re.match(pattern, r)
            lflag = True
            if (j):
                condition = f"Email='{updatede}'"
                customer.execute(f'''select * from Registration where {condition}''')
                r = customer.fetchall()
                if (r != []):
                    lflag = False
                    retur = False
                # for x in customerlist:
                #   if (r == x.email):
                #      lflag=False
                #     retur = False
            if lflag:
                if j:
                    condition = f"Customer_ID='{idval}'"
                    customer.execute(f'''Update Registration SET Email='{updatede}' where {condition}''')
                    con.commit()
                else:
                    inp = "Invalid Credentials Email should be in this format(example@anything.com)"
                    print_box(inp)
                    retur = False
            else:
                inp = "email Id already exists Kindly Change the email"
                print_box(inp)

        elif cho == 3:

            pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%*&?^])[A-Za-z\d!@#$%^&*?]{8,12}$'
            if (re.match(pattern, updatede)):
                condition = f"Customer_ID='{idval}'"
                customer.execute(f'''Update Registration SET Password='{updatede}' where {condition}''')
                con.commit()
                retur = True
            else:
                inp = "Password should be 8-12 letters with one from each \n     1 Upper case \n     2 Lower case \n     3 Special Character \n     4 Numeric Value\n"
                print_box(inp)
                retur = False


        elif cho == 4:

            if (len(updatede) > 100):
                inp = "Invalid Credentials Cannot Update the Address"
                print_box(inp)
                retur = False
            elif (updatede):
                condition = f"Customer_ID='{idval}'"
                customer.execute(f'''Update Registration SET Address='{updatede}' where {condition}''')
                con.commit()
                retur = True

            else:
                inp = "Address Cannot Be Blank"
                print_box(inp)
                retur = False

        elif cho == 5:
            if (len(str(updatede)) != 10):
                inp = "Invalid Credentials Cannot Update the Contact Number"
                print_box(inp)
                retur = False
            else:
                condition = f"Customer_ID='{idval}'"
                customer.execute(f'''Update Registration SET Contact_Number='{updatede}' where {condition}''')
                con.commit()
                retur = True
    else:
        retur = True
        return retur

    if retur:
        inp = "Your Details updated successfully"
        print_box(inp)


def removeCustomer(customerlist):
    cust = int(input("Enter the Customer id:"))
    customer.execute(f'''select * from Registration where {condition}''')
    r = customer.fetchall()
    if (r == []):
        print_box("Incorrect ID")
    else:
        customer.execute(f'''Delete from Registration where {condition}''')
        con.commit()
        inp = "Profile Deleted Successfully"
        print_box(inp)


def inactive(customerlist, id):
    condition = f"Customer_ID='{id}'"
    customer.execute(f"select * from Registration where {condition}")
    r = customer.fetchone()
    if (r == []):
        print_box("Incorrect ID")
    else:
        customer.execute(f"select Status from Registration where {condition}")
        status = customer.fetchone()

        if status[0] == "Active":
            customer.execute(f'''update Registration set Status='Inactive' where {condition}''')
            con.commit()
            inp = "Your Profile is Deactivated Successfully"
            print_box(inp)
            main_menu()


def activate(customerlist, ids):
    condition = f"Customer_ID='{ids}'"
    customer.execute(f'''update Registration set Status='Active' where {condition}''')
    con.commit()
    inp = "Your Profile is Activated Successfully"
    print_box(inp)


def newproduct():
    flag = True
    while flag:
        Id = int(input("Product ID : "))
        condition = f"Product_ID='{Id}'"
        customer.execute(f'''select * from Products where {condition}''')
        r = customer.fetchall()
        if (r != []):
            inp = "Product with this Id already exists"
            print_box(inp)
        else:
            name = input("Product Name : ")
            desc = input("Product Description : ")
            quan = int(input("Quantity : "))
            price = int(input("Price : "))
            customer.execute(
                '''Insert Into Products(Product_ID,Product_Name,Description,Quantity,Price) values(?, ?, ?, ?, ?)''',
                (Id, name, desc, quan, price))
            customer.execute('''select * from Products''')
            r = customer.fetchall()
            table_data = [["Id", "name", "desc", "quan", "price"]]
            for row in r:
                table_data.append(list(row))
                print(tabulate(table_data, headers="firstrow", tablefmt="fancy_grid"))
            con.commit()
            p = Product(Id, name, desc, quan, price)
            return p


def updateProduct(c, value, id):
    if c == 1:
        flag = True
        while flag:
            Id = int(input("Product ID : "))
            condition = f"Product_ID='{Id}'"
            customer.execute(f'''select * from Products where {condition}''')
            r = customer.fetchall()
            if (r != []):
                inp = "Product with this Id already exists"
                print_box(inp)
            else:
                customer.execute('''Update Products SET Product_ID = ? Where Product_ID == ? ''', (value, id))
                flag = False

    elif c == 2:
        customer.execute('''Update Products SET Product_Name = ? Where Product_ID == ? ''', (value, id))
    elif c == 3:
        customer.execute('''Update Products SET Description = ? Where Product_ID == ? ''', (value, id))
    elif c == 4:
        customer.execute('''Update Products SET Quantity = ? Where Product_ID == ? ''', (value, id))
    else:
        customer.execute('''Update Products SET Price = ? Where Product_ID == ? ''', (value, id))

    customer.execute('''select * from Products''')
    r = customer.fetchall()
    table_data = [["Id", "name", "desc", "quan", "price"]]
    for row in r:
        table_data.append(list(row))
        print(tabulate(table_data, headers="firstrow", tablefmt="fancy_grid"))
    con.commit()
    for i in productlist:
        if i.ID == id:
            if c == 1:
                i.ID = value
            elif c == 2:
                i.name = value
            elif c == 3:
                i.desc = value
            elif c == 4:
                i.quan = value
            else:
                i.price = value
    return True


def removeProduct(id, productlist):
    customer.execute('''select * from Products where Product_ID == ?''', (id,))
    r = customer.fetchall()
    if r == []:
        print_box("Product Not available")
        return False
    else:
        customer.execute('''Delete from Products where Product_ID == ?''', (id,))
        con.commit()

        table_data = [["Id", "name", "desc", "quan", "price"]]
        customer.execute('''select * from Products''')
        a = customer.fetchall()
        for row in a:
            table_data.append(list(row))
            print(tabulate(table_data, headers="firstrow", tablefmt="fancy_grid"))
        return True


def findMail(customer_list, mail):
    customer.execute(
        "SELECT Customer_Name, Email, Address, Contact_Number, Customer_id FROM Registration where Email == ? ",
        (mail,))
    r = customer.fetchall()
    headers = ["Name", "Email", "Address", "Contact Number", "Customer ID"]
    if r == []:

        return None
    else:
        return r


def Pricemax(prductobjarray):
    customer.execute('''select max(Price) from Products ''')
    r = customer.fetchone()
    value = r[0]
    return value


def sort_prod(product_list):
    customer.execute('''select * from Products''')
    r = customer.fetchall()
    if r == []:
        print_box("Product Not available")
        return None
    else:
        customer.execute('''select * from Products Order by Quantity Desc''')
        res = customer.fetchall()

    return res


def findDomain(customer_list, domain):
    domain = "%" + domain + "%"
    customer.execute(
        "SELECT Customer_Name, Email, Address, Contact_Number, Customer_id FROM Registration where Email Like ? ",
        (domain,))
    r = customer.fetchall()
    headers = ["Name", "Email", "Address", "Contact Number", "Customer ID"]
    if r == []:
        return None
    else:
        return r


def add_to_cart(productlist, prod_id, prod_quan, cust_id):
    value = True
    customer.execute('''select * from Products where Product_ID == ?''', (prod_id,))
    r = customer.fetchall()
    if r == []:
        print_box("Product Not available")
        value = False
    else:
        customer.execute('''select Quantity from Products where Product_ID == ?''', (prod_id,))
        a = customer.fetchone()
        print(a[0])

        if int(a[0]) < prod_quan:
            inp = "No Stock Available"
            print_box(inp)
            value = False
        else:
            # print(r)
            name = customer.execute('''select Product_Name from Products where Product_ID == ?''', (prod_id,))
            name = name.fetchone()
            des = customer.execute('''select Description from Products where Product_ID == ?''', (prod_id,))
            des = des.fetchone()
            pri = customer.execute('''select Price from Products where Product_ID == ?''', (prod_id,))
            pri = pri.fetchone()
            pric = pri[0] * prod_quan
            customer.execute(
                '''Insert Into Cart(Product_ID,Product_Name,Description,Quantity,Price,Customer_id) values(?, ?, ?, ?, ?, ?)''',
                (prod_id, name[0], des[0], prod_quan, pric, cust_id))
            customer.execute('''Update Products SET Quantity = Quantity-? Where Product_ID == ? ''',
                             (prod_quan, prod_id))
            customer.execute('''select * from Cart Where Customer_id == ? ''', (cust_id,))
            v = customer.fetchall()
            print(v)
            print("Cart items")
            con.commit()
            value = True
    return value


def testingcus(cuslists):
    customer.execute("SELECT Customer_Name, Email, Address, Contact_Number, Customer_id FROM Registration")
    rows = customer.fetchall()

    headers = ["Name", "Email", "Address", "Contact Number", "Customer ID"]
    data = []
    for row in rows:
        data.append(row)

    print(tabulate(data, headers=headers, tablefmt="rounded_grid").center(100))
    print('\n')


def testingprod(prodlist):
    table = []
    table_data = [['Product ID', 'Product Name', 'Description', "Quantity", "Price"]]
    customer.execute('''select * from Products''')
    a = customer.fetchall()
    for row in a:
        table_data.append(list(row))
    print(tabulate(table_data, headers="firstrow", tablefmt="fancy_grid"))


def testingOrder(custid):
    print("\n")
    table_data = [['Order ID', 'Order Date', "Total Price"]]
    customer.execute('''select Order_ID,Order_Date,Amount from Orders where Customer_ID == ?''', (custid,))
    a = customer.fetchall()
    if a == []:
        print_box("No Order Placed")
    else:
        for row in a:
            table_data.append(list(row))
            print(tabulate(table_data, headers="firstrow", tablefmt="fancy_grid"))


def customerregister(customerlist):
    inp = "Kindly register here "
    print_box(inp)

    k = newregister()
    customerlist.append((k))

    main_menu()


def admincustomerregister(customerlist):
    inp = "Kindly register here "
    print_box(inp)

    k = newregister()
    customerlist.append((k))


def login(customerlist, cusid, password):
    value = False
    condition = f"Customer_ID='{cusid}'"
    customer.execute(f'''select * from Registration where {condition}''')
    r = customer.fetchall()
    if (r == []):
        print_box("No Customer With This ID Exists")
    else:
        condition = f"Customer_ID='{cusid}' and Password='{password}'"
        customer.execute(f'''select * from Registration where {condition}''')
        r = customer.fetchall()
        if (r == []):
            print_box("Incorrect Password")
        else:
            condition = f"Customer_ID='{cusid}' and  Status='Active' "
            customer.execute(f'''select * from Registration where {condition}''')
            r = customer.fetchall()
            if (r == []):
                inp = "Your Account state is Inactive"
                print_box(inp)
                value = int(input("If You Wish to Activate press 1 : "))
                if value == 1:
                    condition = f"Customer_ID='{cusid}'"
                    customer.execute(f'''update Registration set Status='Active' where {condition}''')
                    con.commit()
                    value = True
            else:
                inp = "Login Successful"

                print_box(inp)
                customer.execute('''select * from Registration''')
                r = customer.fetchall()
                table_data = [["name", "email", "password", "address", "contact_no", "c_id", "Status"]]
                for row in r:
                    table_data.append(list(row))
                print(tabulate(table_data, headers="firstrow", tablefmt="fancy_grid"))
                value = True
    return value


def admin_login(admin_list, id, passw):
    flag = False
    for each in admin_list:
        if each.id == id:
            if each.password == passw:
                inp = "Login Successful"
                print_box(inp)
                flag = True
    if flag == False:
        inp = "Invalid Credentials"
        print_box(inp)
    return flag


def catluloglist(productlist, category):
    table_data = [['Product ID', 'Product Name', 'Description', "Quantity", "Price"]]
    customer.execute('''select * from Products where Description==?''', (category,))
    a = customer.fetchall()
    if a == []:
        return None
    else:
        return a


def srcCustbyName(customerlist, k):
    # personDetails=[]
    #    for i in customerlist:
    #        nm = i.name
    #        if k.lower() in nm.lower():
    #            personDetails.append(i)
    #    return personDetails

    customer.execute(
        '''SELECT Customer_Name, Email, Address, Contact_Number, Customer_id FROM Registration WHERE Customer_Name LIKE ?''',
        ('%' + k + '%',))
    custData = customer.fetchall()
    table_data = [["name", "email", "password", "address", "contact_no", "c_id", "Status"]]
    if custData:
        for row in custData:
            table_data.append(list(row))
        print(tabulate(table_data, headers="firstrow", tablefmt="rounded_grid").center(100))
    else:
        print("No Such Customer")


def find_customer_name(letter, customerlist):
    customer_data = {}
    for customer in customerlist:
        name = customer.name
        if name.lower()[0] == letter.lower():
            customer_data[name] = customer.address

    if len(customer_data) == 0:
        print_box("No such Customer")
    else:
        print_box("Customer Found")
        # print('\n')
        headers = ["Customer Name", "Address"]
        table = []
        for k, v in customer_data.items():
            table.append([k, v])
        print(tabulate(table, headers, tablefmt="rounded_grid").center(100))
        print('\n')

    return 0


def productfilter(productlist):
    table = []
    flag = False
    inp = input("Enter the product name: ").lower()
    print("\n")
    for i in productlist:
        if i.name.lower() == inp:
            table.append(i)
            flag = True
    if flag:
        return table
    else:
        return None
    customer.execute('''SELECT Product_id, Product_Name, Price, Description FROM Products WHERE Product_Name LIKE ?''',
                     ('%' + inp + '%',))
    results = c.fetchall()
    for i in results:
        print(list(i))


def catfilter(productlist):
    table = []
    flag = False
    inp = input("Enter the category: ")
    print('\n')
    for i in productlist:
        if i.desc == inp:
            table.append(i)
            flag = True
    if flag:
        return table
    else:
        return None


def pricefilter(productlist, c):
    table = []
    flag = False
    if c == 1:
        pri = int(input("Enter the price: "))
        print("\n")
        for i in productlist:
            if i.price > pri:
                table.append(i)
                flag = True
    if c == 2:
        pri = int(input("Enter the price: "))
        print("\n")
        for i in productlist:
            if i.price < pri:
                table.append(i)
                flag = True
    if c == 3:
        apri = int(input("Enter the Above price: "))
        bpri = int(input("Enter the Below price: "))
        print("\n")
        for i in productlist:
            if i.price > apri and i.price < bpri:
                table.append(i)
                flag = True
    if flag:
        return table
    else:
        return None


def searchfiltering(productlist):
    l = ['\n1.Based on name', "2.Based on category", '3.Based on Price range']
    headers = ['Product ID', 'Product Name', "Price", "Quantity"]
    table = []
    for i in l:
        print(i)
    print('\n')
    choice = int(input("Enter the choice: "))
    if choice == 1:
        k = productfilter(productlist)
        if k != None:
            testingprod(k)
        else:
            inp = "Product not Found"
            print_box(inp)

    if choice == 2:
        k = catfilter(productlist)
        if k != None:
            testingprod(k)
        else:
            inp = "Category not Found"
            print_box(inp)

    if choice == 3:
        lis = ['\n1.Above the Given price', "2.Below the Given price", '3.Between Given Range']
        for i in lis:
            print(i)
        print('\n')
        c = int(input("Enter the choice: "))
        print('\n')
        k = pricefilter(productlist, c)
        if k != None:
            testingprod(k)
        else:
            inp = "No Product Found"
            print_box(inp)


customerlist = []
productlist = []
cartlist = []
adminlist = []
orderdetails = []
customerlist.append(Customer("cust", "cust@tcs", "123456", "Chennai", "1234567890", 12345))
customerlist.append(Customer("cust2", "cust2@tcs.com", "5678901", "Chennai", "1234567890", 12346))
adminlist.append(Admin('admin', '123456', 12345))
adminlist.append(Admin('admin2', 'admin2@tcs', 56789))
productlist.append(Product(102, "Apple", "Fruit", 12, 50))
productlist.append(Product(104, "Orange", "Fruit", 16, 30))
productlist.append(Product(106, "Grapes", "Fruit", 10, 70))
productlist.append(Product(107, "Tomato", "Vege", 40, 30))
productlist.append(Product(108, "Bitter Guard", "Vege", 20, 45))
productlist.append(Product(109, "Potato", "Vege", 12, 60))
productlist.append(Product(110, "Dhal", "Cerals", 17, 170))
productlist.append(Product(111, "Hourse Gram", "Cerals", 13, 70))
productlist.append(Product(116, "Badam", "Nuts", 18, 460))
productlist.append(Product(118, "Pista", "Nuts", 17, 600))


def customermain(customerlist, cartlist, productlist, customer_choice, orderdetails, custid):
    choice = customer_choice
    sum = 0
    if choice == '1':
        lista = ['\n1.Update Name', "2.Update e-mail", '3.Update password', '4.Address', '5.Contact number\n']
        for i in lista:
            print(i)
        choice = int(input("Click the number to update : "))
        valtopass = None
        if choice == 5:
            valtopass = int(input("Enter the Phone number to update : "))
        else:
            valtopass = input('Enter the value to update : ')

        ids = int(input("Enter the Customer ID : "))
        if ids != None:
            k = updateCustomerDetails(customerlist, ids, choice, valtopass)
            if k:
                inp = 'Invalid Data'
                print_box(inp)

    elif choice == '2':
        id = int(input("\nEnter customer ID: "))
        inactive(customerlist, id)

    elif choice == '3':

        n = int(input("\nEnter the number of products to add to cart: "))
        for i in range(n):
            prod_id = int(input("Enter Product ID: "))
            Quan = int(input("Enter Product Quantity: "))
            x = add_to_cart(productlist, prod_id, Quan, custid)

        if len(cartlist) != 0:
            inp = "Product Added Sucessfully"
            # print_box(inp)

        customer.execute('''select Sum(Price) from Cart Where Customer_ID == ? ''', (custid,))
        v = customer.fetchone()
        sum = v[0]

        if sum > 0:
            print(f"Total Amount : {v[0]}".center(100))
            print('\n')
            print("Click 1 tocheckout: ")
            print('\n')
            print("or Press m- main menu or q- quit")
            a = (input("Enter your Choice: "))
            if a == '1':
                TransID = int(random.randint(10000, 99999))
                print_box(f"Transaction successfull Your TransactionID is  {TransID}")
                dat = date.today()
                customer.execute("Drop table Cart")
                customer.execute('''Create Table if not exists Cart(Product_ID int Not null Primary Key,
                	Product_Name varchar(15) Not null,Description varchar(20) Not null,Quantity int Not null,Price int Not null,Customer_id int Not null)''')

                customer.execute('''Insert Into Orders(Order_ID,Order_Date,Amount,Customer_ID) values(?, ?, ?, ?)''',
                                 (TransID, dat, sum, custid))
                customer.execute('''select * from Orders''')
                r = customer.fetchall()
                table_data = [["Order ID", "OrderDate", "Amount", "Customer ID"]]
                for row in r:
                    table_data.append(list(row))
                print(tabulate(table_data, headers="firstrow", tablefmt="fancy_grid"))
                con.commit()
                orderdetails.append(OrderDetails(TransID, date.today(), sum, custid))

                cartlist = []
                testingprod(cartlist)

            elif (a == 'm' or a == 'q'):
                if a == 'q':
                    inp = 'Thanks for Shopping with us, We wait for your next vist.'
                    con.close()
                    print_box(inp)
                    exit()
                if a == 'm':
                    pass
        else:
            print_box("Cart is Empty")



    elif choice == '4':
        inp = "Product Details"
        inp = print_box(inp)
        testingprod(productlist)

    elif choice == '5':
        customer.execute(" select * from Cart")
        v = customer.fetchall()
        if v != []:
            inp = "Products in cart"
            inp = print_box(inp)
            table_data = [['Product ID', 'Product Name', "Quantity", "Price"]]
            for row in v:
                table_data.append(list(row))
            print(tabulate(table_data, headers="firstrow", tablefmt="fancy_grid"))
        else:
            print_box("Cart is Empty")

    elif choice == '6':
        print("The available Categories are:")
        print("1 . Vege")
        print("2 . Fruit")
        print("3 . Cerals")
        print("4 . Nuts")

        print("\n")
        value = input("Enter the Category Name to search : ")
        print("\n")
        res = catluloglist(productlist, value)
        if res != None:
            table_data = [["Order ID", "OrderDate", "Description", "Amount", "Customer ID"]]
            for row in res:
                table_data.append(row)
            print(tabulate(table_data, headers="firstrow", tablefmt="fancy_grid"))
        else:
            print_box("Enter Correct Category")
    elif choice == '7':
        searchfiltering(productlist)

    elif choice == "8":
        testingOrder(custid)






    elif (choice == 'm' or choice == 'q'):

        if choice == 'q':
            inp = 'Thanks for Shopping with us, We wait for your next vist.'
            print_box(inp)
            cartlist = []
            con.close()
            exit()
        if choice == 'm':
            cartlist = []
            main_menu()
    else:
        inp = "Invalid Input"
        print_box(inp)

    customer_choice = customer_services()
    customermain(customerlist, cartlist, productlist, customer_choice, orderdetails, custid)


def Adminmain(customerlist, productlist, admin_choice):
    choice = admin_choice
    if choice == '1':
        print("Kindly Add Products here ")
        k = newproduct()
        productlist.append(k)
        inp = 'Product Registered successful'
        print_box(inp)
        testingprod(productlist)

    elif choice == '2':
        email = input("Enter the mail to Search : ")
        res = findMail(customerlist, email)
        if res == None:

            inp = 'No such customer'
            print_box(inp)

        else:

            inp = "Customer found"
            headers = ["Name", "Email", "Address", "Contact Number", "Customer ID"]
            data = []
            for row in res:
                data.append(row)

            print(tabulate(data, headers=headers, tablefmt="rounded_grid").center(100))
            print('\n')




    elif choice == '3':
        res = Pricemax(productlist)
        inp = f"The Product with highest price : {res}".center(100)
        print_box(inp)
        customer.execute('''select * from Products where Price== ? ''', (res,))
        r = customer.fetchall()
        headers = ['Product ID', 'Product Name', 'Description', "Price", "Quantity"]
        data = []
        for row in r:
            data.append(row)

        print(tabulate(data, headers=headers, tablefmt="rounded_grid").center(100))
        print('\n')


    elif choice == '4':
        if len(productlist) != 0:
            res = sort_prod(productlist)
            print("\n")
            headers = ['Product ID', 'Product Name', 'Description', "Quantity", "Price"]
            data = []
            for row in res:
                data.append(row)

            print(tabulate(data, headers=headers, tablefmt="rounded_grid").center(100))
            print('\n')

        else:
            sent = "Product List is Empty"
            productlist(sent)

    elif choice == '5':
        domain = input("Enter the domain: ")
        print("\n")
        value = findDomain(customerlist, domain)
        if value != None:
            inp = "Customer found"
            headers = ["Name", "Email", "Address", "Contact Number", "Customer ID"]
            data = []
            for row in value:
                data.append(row)

            print(tabulate(data, headers=headers, tablefmt="rounded_grid").center(100))
            print('\n')

        else:
            sent = "No such Customer"
            print_box(sent)

    elif choice == '6':
        inp = 'Customer Details'
        print_box(inp)
        testingcus(customerlist)

    elif choice == '7':
        admincustomerregister(customerlist)


    elif choice == '8':
        lista = ['\n1.Update Name', "2.Update e-mail", '3.Update password', '4.Address', '5.Contact number\n']
        for i in lista:
            print(i)
        choice = int(input("Click the number to update : "))
        valtopass = None
        if choice == 5:
            valtopass = int(input("Enter the Phone number to update : "))
        else:
            valtopass = input('Enter the value to update : ')

        ids = int(input("Enter the Customer ID : "))
        if ids != None:
            k = updateCustomerDetails(customerlist, ids, choice, valtopass)
            if k:
                inp = 'Invalid Data'
                print_box(inp)

    elif choice == '9':
        x = removeCustomer(customerlist)
        if x:
            inp = "Account Deleted successfully"
            print_box(inp)
        else:
            inp = "Invalid customer id"
            print_box(inp)

    elif choice == '10':
        x = input("\nEnter letter to search : ")
        find_customer_name(x, customerlist)

    elif choice == '11':
        lis = ['\n1. Update Product_ID', '2. Update Product_Name', '3. Update_Description', '4. Update_Quantity',
               '5. Update Price\n']
        for i in lis:
            print(i)
        choice = int(input("Enter the Choice: "))
        valtopass = None
        if choice == 2 or choice == 3:
            valtopass = input("Enter the value to update : ")
        elif choice == 1 or choice == 4 or choice == 5:
            valtopass = int(input('Enter the value to update : '))
        else:
            print_box("Invalid Choice")
        ids = int(input("Enter the Product ID : "))
        if ids != None:
            x = updateProduct(choice, valtopass, ids)
            if x:
                inp = "Product Updated successfully"
                print_box(inp)
            else:
                inp = "Invalid Product id"
                print_box(inp)

    elif choice == '12':
        y = input("\nEnter the Product Id: ")
        x = removeProduct(y, productlist)
        if x:
            inp = "Product Deleted successfully"
            print_box(inp)
        else:
            inp = "Invalid Product id"
            print_box(inp)

    elif choice == '13':
        k = input("\nEnter the Customer Name : ")
        m = srcCustbyName(customerlist, k)

        # if len(m) == 0:
    #            print_box("No such Customer")
    #        else:
    #            print_box("Customer Found")
    #            testingcus(m)

    elif (choice == 'm' or choice == 'q'):

        if choice == 'q':
            con.close()
            exit()
        elif choice == 'm':
            main_menu()

    else:
        sent = "Invalid Input"
        print_box(sent)

    admin_choice = admin_services()
    Adminmain(customerlist, productlist, admin_choice)


def customer_services():
    # print("\n\t\t\t\t\t Customer Services\t\t\t".center(50))
    print('-----------------'.center(100))
    print("Customer Services".center(100))
    print('-----------------'.center(100))
    print("\n1. Update Customer Details\n2. Deactivate Profile\n3. Add Products to Cart"
          "\n4. List Products\n5. List Cart\n6. List Catelogue\n7. Product Search and Filtering\n8. View Orders Details")
    print("\nPress m - Main Menu or q - Quit")
    return (input('\nEnter your choice : '))


def admin_services():
    print('--------------'.center(100))
    print("Admin Services".center(100))
    print('--------------'.center(100))
    print(
        "\n1. Add product details\n2. Search Customer by Email\n3. Find Product with highest price\n4. Sort Products based on quantity"
        "\n5. Search Customer by Domain\n6. List Customer Details\n7. Add Customer\n8. Update Customer Details\n9. Remove Customer"
        "\n10. Search Customer\n11. Update Product\n12. Remove Product\n13. Search Customer by Name")
    print("\nPress m - Main Menu or q - Quit")
    return (input('\nEnter your choice : '))


def main_menu():
    print('---------'.center(100))
    print("Main Menu".center(100))
    print('---------'.center(100))
    print('Choose user type \n')
    print("1 Customer Login")
    print('2 Customer Register')
    print('3 Admin Login\n')
    print("\nPress q - Quit")

    user_type = input('\nEnter your choice (1,2 or 3): ')

    if user_type == '1':
        custid = int(input("Enter the Customer ID : "))
        Pass = (input("Enter the Password : "))
        k = login(customerlist, custid, Pass)
        cartlist = []
        if k:
            customer_choice = customer_services()
            customermain(customerlist, cartlist, productlist, customer_choice, orderdetails, custid)
        else:
            main_menu()

    if user_type == "2":
        customerregister(customerlist)



    elif user_type == '3':
        custid = int(input("Enter the Admin ID : "))
        Pass = (input("Enter the Password : "))
        x = admin_login(adminlist, custid, Pass)
        if x:
            admin_choice = admin_services()
            Adminmain(customerlist, productlist, admin_choice)
        else:
            main_menu()

    elif user_type == 'q':
        inp = 'Thanks for Shopping with us, We wait for your next vist.'
        print_box(inp)
        con.close()
        exit()

    else:
        print_box('Invalid choice! Please choose 1, 2 or 3')
        main_menu()


def print_box(message):
    box_width = len(message) + 8
    box_top = "╔" + "═" * (box_width - 2) + "╗"
    box_middle = "║" + " " * (box_width - 2) + "║"
    title = f"║   {message}   ║"
    box_bottom = "╚" + "═" * (box_width - 2) + "╝"

    print("\n")
    print(box_top.center(100))
    print(box_middle.center(100))
    print(title.center(100))
    print(box_middle.center(100))
    print(box_bottom.center(100))
    print('\n')


# MAIN METHOD

print(r"""

               ____        _ _               _____                                  _____ _                 
              / __ \      | (_)             / ____|                                / ____| |                
             | |  | |_ __ | |_ _ __   ___  | |  __ _ __ ___   ___ ___ _ __ _   _  | (___ | |_ ___  _ __ ___ 
             | |  | | '_ \| | | '_ \ / _ \ | | |_ | '__/ _ \ / __/ _ \ '__| | | |  \___ \| __/ _ \| '__/ _ \
             | |__| | | | | | | | | |  __/ | |__| | | | (_) | (_|  __/ |  | |_| |  ____) | || (_) | | |  __/
              \____/|_| |_|_|_|_| |_|\___|  \_____|_|  \___/ \___\___|_|   \__, | |_____/ \__\___/|_|  \___|
                                                                            __/ |                           
                                                                           |___/                           
    """)

print('\n')

welcome_message = "Welcome to Online Grocery Store - Your one-stop destination for quality groceries delivered to your doorstep !!"

print_box(welcome_message)
main_menu()
