from flask import Flask, render_template, redirect, request, session,jsonify,g
import re,random
from datetime import datetime
from functools import wraps
import pymysql

hostname = 'database-1.cde4044wig4c.ap-south-1.rds.amazonaws.com'
port = 3306 
dbname = 'Geocery_new'
username = 'Santhosh'
password = 'Iamingood'

con= pymysql.connect(
    host=hostname,
    port=port,
    user=username,
    password=password,
    database=dbname
)
customer=con.cursor()

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = 'your_secret_key'

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        print('wrapper invoked')
        # auth_status = session['custid']
        auth_status = session.get('custid',False)
        if auth_status:
            return f(*args, **kwargs)
        else:
            print('Unauthorized Access')
            # return redirect(url_for('page_not_found'))
            return render_template('401.html')
    return wrap

def admin_login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        print('admin wrapper invoked')
        # auth_status = session['adminid']
        auth_status = session.get('admincustid',False)
        if auth_status:
            return f(*args, **kwargs)
        else:
            print('Unauthorized Admin Access')
            # return redirect(url_for('page_not_found'))
            return render_template('401.html')
    return wrap

 
@app.route('/login-validate', methods=["POST"])
def loginValidate():
    print("login request received")
    print("JSON Value", request.json)

    if request.method == "POST":
        cid = request.json.get("userid")
        pwd = request.json.get("password")
        res = user_login(cid, pwd)
        print(res)

        if res.get("validity") == "valid":
            session.pop('custid',None)
            session['custid'] = cid
            print(session['custid'])

        return jsonify(res)

@app.route('/register-validate',methods=["POST"])
def registerValidate():
    print("login request received")
    print("JSON Value", request.json)
    print("Register request recieved")
    print("JSON Value", request.json)
    if request.method == "POST":
        name = request.json.get("userName")
        pwd = request.json.get("userPassword")
        email = request.json.get("userEmail")
        cid = request.json.get("customerId")
        contact = request.json.get("usernumber")
        address = request.json.get("userAddress")
    res = newregister(name, email, pwd, address, contact, cid)
    print(res)
    print(f"UID - {cid} \nPassword - {pwd}")
    return jsonify(res)

@app.route('/add-wish',methods=["POST"])
def add_to_wish():
    print("wish request recieved")
    print("JSON Value", request.json)
    if request.method == "POST":
        product_id = request.json.get("pid")
        product_name = request.json.get("pname")
        product_desc = request.json.get("desc")
        product_quant = request.json.get("quant")
        product_price = request.json.get("price")
        customer_id = session["custid"]
    customer.execute('''select * from Wishlist where Product_ID =%s''', (product_id,))
    r = customer.fetchall()
    if (r != ()):
        _message = "Product already added to Wishlist"
        _status = "invalid"
    else:
        _message = "Product added Successfully"
        _status = "valid"

        customer.execute(
            '''Insert Into Wishlist(Product_ID,Product_Name,Description,Quantity,Price, Customer_id) values(%s, %s, %s, %s, %s, %s)''',
            (product_id, product_name, product_desc, product_quant, product_price, customer_id))
        con.commit()

    return jsonify({"name": product_name, "customer": product_id, "status": _status,
                    "message": _message})

@app.route('/logout')
def logout():
    session.pop("custid",None)
    session.pop('admincustid', None)
    session.pop('password',None)
    session.pop("adminid",None)
    return redirect("/login")




@app.route('/add-cart',methods=["POST"])
def add_to_cart():
    print("cart request recieved")
    print("JSON Value",request.json)
    if request.method == "POST":
        product_id = request.json.get("pid")
        product_name = request.json.get("pname")
        product_desc = request.json.get("desc")
        product_quant = request.json.get("quant")
        product_price = request.json.get("price")
        customer_id = session['custid']
    customer.execute(f'''select * from Cart where Product_ID =%s and Customer_id=%s''', (product_id,customer_id,))
    r = customer.fetchall()
    print(r,"here")
    if (r != ()):
        print("hello")
        _message = "Product already added"
        _status = "invalid"
    elif r==():
        customer.execute(f'''select Quantity  from Products where Product_ID =%s''', (product_id,))
        quan=customer.fetchone()
        if quan[0]==0:
            _message = "Product out of Stock"
            _status = "nostock"

        else:
            _message = "Product added Successfully"
            _status = "valid"
            customer.execute(
                f'''Insert Into Cart(Product_ID,Product_Name,Description,Quantity,Price, Customer_id) values(%s, %s, %s, %s, %s, %s)''', (product_id, product_name, product_desc, product_quant, product_price,customer_id))
            customer.execute("Update Products set Quantity=Quantity-1 where Product_Id=%s", (product_id,))
            con.commit()

    print((product_id, product_name, product_desc, product_quant, product_price))

    return jsonify({"name" : product_name, "customer" : product_id ,"status": _status,
                        "message": _message})

@app.route('/get-products',methods=["GET"])
def get_products():
    print("get products request recieved")
    # print("JSON Value",request.json)
    customer.execute('''select * from Products''')
    r = customer.fetchall()
    keys_list = ['id', 'name', 'desc', 'quant', 'price']
    temp_dict = {}
    res_list = []
    lis = []
    for each in r:
        res_list.append(list(each))

    for val in res_list:
        temp_dict = dict(zip(keys_list,val))
        lis.append(temp_dict)
    return jsonify({'products' : lis})

@app.route('/check-cart/<prid>',methods=["POST"])
def check_cart(prid):
    print("check cart request recieved")
    # print("JSON Value",request.json)
    # if request.method == "POST":
    #     product_id = request.json.get("pid")
    p_id = prid
    customer.execute('''select * from Cart where Product_ID =%s''', (p_id,))
    r = customer.fetchall()
    if r != []:
        return jsonify({'status' : 'available', 'message' : 'product already added'})
    else:
        return jsonify({'status' : 'not_available', 'message' : 'product not added'})


@app.route('/')
def root():
    return 'Handshake Secured'

@app.route('/login')
def login():
    return render_template('ogc_login.html')

@app.route('/register')
def register():
    return render_template('ogc_register.html')

@app.route('/home')
@login_required
def home():
    return render_template('ogc_home.html')

@app.route('/cart')
@login_required
def cart():
    value=session['custid']
    customer.execute(f'''select * from Cart where Customer_id =%s''', (value,))
    r = customer.fetchall()
    print(r)
    print(value)
    return render_template('ogc_cart.html', data=r)

@app.route('/function-cart',methods=["POST"])
def functions_of_Cart():
    value = session['custid']
    funtiopass=request.json.get("fun")
    prodid=request.json.get("id")
    customer.execute('''Select Quantity from Cart  where Product_Id=%s and Customer_id =%s''',(prodid,value))
    r=customer.fetchone()
    quan=r[0]
    print(quan)
    if funtiopass=='rem':
        if quan>1:
            customer.execute("Update Cart set Quantity=Quantity-1 where Product_Id=%s and Customer_id =%s",(prodid,value))
            customer.execute("Update Products set Quantity=Quantity+1 where Product_Id=%s", (prodid,))
            con.commit()
        elif quan==1:
            customer.execute("Delete from Cart where Product_Id=%s and Customer_id =%s",(prodid,value))
            con.commit()

    elif funtiopass=='add':
        customer.execute('''Select Quantity from Products  where Product_Id=%s''', (prodid,))
        r = customer.fetchone()
        pquan = r[0]
        print(pquan)
        if pquan>0:
            customer.execute("Update Cart set Quantity=Quantity+1 where Product_Id=%s and Customer_id =%s",(prodid,value))
            customer.execute("Update Products set Quantity=Quantity-1 where Product_Id=%s", (prodid,))
            con.commit()
            return jsonify({"Status":200,"product_quan":pquan})

        elif pquan==0:
            print("hello")
            return jsonify({"errors": 'Out of stock',"Status":201,"product_quan":pquan})

    elif funtiopass == 'totrem':
        customer.execute("select Quantity from Cart where Customer_id=%s and Product_Id=%s",(value,prodid))
        qaunt=customer.fetchone()
        customer.execute("Delete from Cart where Product_Id=%s and Customer_id =%s",(prodid,value))
        customer.execute("Update Products set Quantity=Quantity+%s where Product_Id=%s", (qaunt[0],prodid,))
        con.commit()
        return jsonify({"Status": 200, "message": "Removed Succesfully"})


@app.route('/display_product_details', methods=["POST"])
def display_product():
    pid = request.json.get("pid")
    session['adminprodid'] = pid
    customer.execute('Select * from Products where Product_ID =%s', (pid,))
    a = customer.fetchone()
    print(a)
    if a == None:
        return jsonify({"message": "No Products Found", "Status": 201})
    elif a != None:
        return jsonify(
            {"pid": a[0], "name" : a[1], "desc": a[2], 'quant': a[3], "price": a[4], "Status": 200, "message": "Product Found"})



@app.route('/invoice',methods=['POST'])
def invoice():
    paymethod = request.form.get('payment')
    if(paymethod=="Cash on Delivery"):
        co = session.get('total')
        x = co[0] - ((co[0] * 20) / 100) + ((co[0] * 12) / 100) + 10
        x = "{:.2f}".format(x)
        tr = int(random.randint(10000, 99999))
        custid = session['custid']
        date = str(datetime.now().date())
        customer.execute("insert into Orders values (%s, %s, %s, %s, %s)", (tr, date, x, custid, paymethod))
        customer.execute('delete from Cart where Customer_Id=%s', (custid,))
        con.commit()
        return render_template('ogc_home.html')
    if(paymethod):
        value = session['custid']
        condition = f"Customer_id='{value}'"
        customer.execute(f'''select Product_Name,Product_ID from Cart where {condition}''')
        r=customer.fetchall()
        k=len(r)
        co=session.get('total')
        co=int(co[0])
        x = co - ((co * 20) / 100) + ((co * 12) / 100) + 10
        x="{:.2f}".format(x)
        tr=int(random.randint(10000, 99999))
        date = str(datetime.now().date())
        customer.execute("insert into Orders values (%s, %s, %s, %s, %s)", (tr, date, x, value, paymethod))
        customer.execute('delete from Cart where Customer_Id=%s', (value,))
        con.commit()
        return render_template('ogc_invoice.html', proname=r, total=x, tr=tr, Customer_id=value, k=k)
        #return redirect(url_for('invoice'))
    else:
        value=session['custid']
        condition = f"Customer_id='{value}'"
        customer.execute(f'''select sum(Price) from cart where {condition}''')
        r = customer.fetchall()
        session['total'] = r[0]
        return render_template('ogc_transaction.html', r=r[0])
        #return render_template('ogc_transaction.html')



@app.route("/wishlist")
@login_required
def wishlist():
    value = session['custid']
    customer.execute(f'''select * from Wishlist where Customer_id =%s''', (value,))
    r = customer.fetchall()
    return render_template("ogc_wishlist.html",data=r)

@app.route("/wish-function",methods=["POST"])
def functions_of_wish():
    value = session['custid']
    funtiopass = request.json.get("fun")
    prodid = request.json.get("id")
    print(funtiopass,prodid)
    if funtiopass == 'totrem':
        print(funtiopass,"Hello i am worked")
        customer.execute("Delete from Wishlist where Product_Id=%s and Customer_id=%s", (prodid,value))
        con.commit()
        return jsonify({"Status": 200, "message": "Removed Succesfully"})
    elif funtiopass=='add':
        customer.execute('''Select * from Cart  where Product_Id=%s and Customer_id=%s''', (prodid,value))
        val = customer.fetchall()
        print(val)
        if val==():
            customer.execute("select * from Products where Product_ID=%s",(prodid,))
            r=customer.fetchone()
            customer.execute("Insert into Cart values(%s,%s,%s,%s,%s,%s)",(r[0],r[1],r[2],1,r[4],value))
            con.commit()
            print("Im worked",r)
            return jsonify({"Status":200,"message":"Product Added to cart"})
        elif val!=():
            return jsonify({"errors": 'Already in cart',"Status":201})


@app.route('/profile-update')
@login_required
def profile_update():
    value = session['custid']
    customer.execute(f'''select * from Registration where Customer_id =%s''', (value,))
    r = customer.fetchone()
    return render_template('ogc_profileupdate.html', name=r[0], email=r[1],passw=r[2], address=r[3], contact=r[4])


@app.route('/update-profile',methods=["POST"])
def update_profile():
    #named
    updatede=request.json.get('name')
    condition=session['custid']
    email = (request.json.get('email'))
    password = request.json.get("password")
    address=request.json.get('address')
    phone=request.json.get('contact')
    print(updatede,condition,email),print(password,address,phone)
    case=0
    for i in range(len(updatede)):
        if (ord(updatede[i]) > 32 and ord(updatede[i]) < 65):
            case = 1
            break

    if (case == 1):
        return jsonify({"errors":"Name should not contain any Special characters or Numeric Values","Status":201})

    if case==0:
        if (len(updatede) < 50):
            customer.execute(f'''Update Registration SET Customer_Name='{updatede}' where Customer_id={condition}''')
            con.commit()
            #return jsonify({'message':"Updation Sucess" ,"Status":200})
        else:
            return jsonify({"errors":"Name should be less than 50 letters","Status":201})
    #email
    
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z.-]+\.\b'
    j = re.match(pattern, email)
    lflag = True
    if (j):
        pass

    if lflag:
        if j:
            customer.execute(f'''Update Registration SET Email='{email}' where  Customer_id={condition}''')
            con.commit()
            #return jsonify({'message': "Updation Sucess", "Status": 200})
        else:
            return jsonify({"errors":"Invalid Credentials Email should be in this format(example@anything.com)","Status":201})

    if not lflag:
        return jsonify({"errors":"email Id already exists Kindly Change the email","Status":201})
    
    #password
    
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,12}$'
    print(len(password))
    if re.match(pattern, password):
        customer.execute(f'''Update Registration SET Password='{password}' where  Customer_id={condition}''')
        con.commit()
        return jsonify({'message': "Updation Sucess", "Status": 200})
    if not (re.match(pattern, password)):
       return jsonify({"errors":"Password does not meet the criteria","Status":201})
    #address
    if (len(address) > 100):
        return jsonify({"errors":"Invalid Credentials Cannot Update the Address","Status":201}) 
    elif (address):
        customer.execute(f'''Update Registration SET Address='{address}' where Customer_id=={condition}''')
        con.commit()
        #return jsonify({'message': "Updation Sucess", "Status": 200})
    if len(address)==0:
        return jsonify({"errors":"Address Cannot Be Blank",'Status':201})
    #contact
    pattern = r'^[0-9]\d{9}$'
    if re.match(pattern, phone):
        customer.execute(f'''Update Registration SET Contact_Number='{phone}' where  Customer_id=={condition}''')
        con.commit()
        return jsonify({'message': "Updation Success", "Status": 200})

    if not re.match(pattern, phone):
        return jsonify({"errors":"Cannot Update the Contact Number","Status":201})


def newregister(name, email, password, address, contact_no, c_id):
    flag = True
    # email

    condition = f"Email='{email.lower()}'"
    customer.execute(f'''select * from Registration where {condition}''')
    r = customer.fetchall()
    if (r != ()):
        return {"message": "email Id already exists Kindly Change the email","status" : "invalid"}

    # customer z
    customer.execute('''Insert Into Registration(
	Customer_Name,Email,Password,Address,Contact_Number,
    Customer_ID,Status) values(%s, %s, %s, %s, %s, %s, %s)''', (name, email, password, address, contact_no, c_id, 'Active'))
    con.commit()
    return {"customer" : c_id ,"status" : 'valid',"message" : "Registration Successful"}

def user_login(cusid,password):
    value = False
    condition = f"Customer_ID='{cusid}'"
    customer.execute(f'''select * from Registration where {condition}''')
    r = customer.fetchall()

    if (r == ()):
        return { "name" : "null", "customer" : cusid , "status" : "invalid",
            "message" : "Customer ID not found" }
    else:
        condition = f"Customer_ID='{cusid}' and Password='{password}'"
        customer.execute(f'''select * from Registration where {condition}''')
        r = customer.fetchall()
        if (r == ()):
            print("Incorrect Password")
            return {"name" : "null", "customer" : cusid ,"status": "invalid","validity":"invalid",
                    "message": "Incorrect Password"}
        else:
            condition = f"Customer_ID='{cusid}' and Status='Active'"
            customer.execute(f'''select * from Registration where {condition}''')
            r = customer.fetchall()
            if (r == ()):
                session['custid'] = cusid
                inp = "Your Account state is Inactive"
                return {"name" : "null", "customer" : cusid ,"status": "Inactive","validity":"valid",
                        "message": "Your Account state is Inactive"}
            else:
                inp = "Login Successful"
                print(inp)
                # customer.execute('''select * from Registration''')
                # r = customer.fetchall()
                # table_data = [["name", "email", "password", "address", "contact_no", "c_id", "Status"]]
                # for row in r:
                #     table_data.append(list(row))
                # print(tabulate(table_data, headers="firstrow", tablefmt="fancy_grid"))
                #
                customer.execute(f'''select Customer_Name from Registration where customer_id = {cusid}''')
                r = customer.fetchall()
                print(r)
                cust_name = str(r[0][0])
                

                value = True
                return {"name" : cust_name, "customer" : cusid ,"status": "valid","validity":"valid",
                        "message": "Login Successful"}
    return value      

@app.route('/profile')
@login_required
def profiles():
    value=session['custid']
    print(value)
    customer.execute(f'''select * from Registration where Customer_id =%s''',(value,))
    r = customer.fetchone()
    return render_template('ogc_profile.html',name=r[0],email=r[1],address=r[3],contact=r[4])

@app.route('/transaction')
@login_required
def transaction():
    value=session['custid']
    condition=f"Customer_id='{value}'"
    customer.execute("SELECT SUM(Price * Quantity) FROM Cart WHERE Customer_id = %s",(value,))
    r=customer.fetchall()
    session['total']=r[0]
    return render_template('ogc_transaction.html',r=r[0])

@app.route('/order')
@login_required
def order():
    customer.execute(f'''select * from Orders where Customer_ID =%s''',(session['custid'],))
    r = customer.fetchall()
    print(r)
    if r!=[]:
        return render_template("ogc_order.html", ta=r)
    elif r==[]:
        return render_template("ogc_noorder.html")


@app.route('/admin-home')
@admin_login_required
def admin_home():
    return render_template("admin_home.html")

@app.route('/admincustregister')
@admin_login_required
def admin_customer_register():
    return render_template('admin_customer_register.html')

@app.route("/admin-update")
@admin_login_required
def admin_update():
    return render_template('admin_customerupdate.html')

@app.route("/admin-remove")
@admin_login_required
def admin_remove():
    return render_template('admin_removecust.html')



@app.route('/admin-profile-update')
@admin_login_required
def admin_profile_update():
    value = session['admincustid']
    customer.execute(f'''select * from Registration where Customer_id =%s''', (value,))
    r = customer.fetchone()
    return render_template('admin_updatedetails.html', name=r[0], email=r[1], passw=r[2], address=r[3], contact=r[4])


@app.route('/admin-update-profile', methods=["POST"])
def admin_update_profile():
    # named
    updatede = request.json.get('name')
    print(session['admincustid'])
    condition = session['admincustid']
    print(condition)
    email = (request.json.get('email'))
    password = request.json.get("password")
    address = request.json.get('address')
    phone = request.json.get('contact')
    #print(updatede, condition, email), print(password, address, phone)
    case = 0
    for i in range(len(updatede)):
        if (ord(updatede[i]) > 32 and ord(updatede[i]) < 65):
            case = 1
            break

    if (case == 1):
        return jsonify({"errors": "Name should not contain any Special characters or Numeric Values", "Status": 201})

    if case == 0:
        if (len(updatede) < 50):
            customer.execute(f'''Update Registration SET Customer_Name='{updatede}' where Customer_id={condition}''')
            con.commit()
            # return jsonify({'message':"Updation Sucess" ,"Status":200})
        else:
            return jsonify({"errors": "Name should be less than 50 letters", "Status": 201})
    # email

    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z.-]+\.\b'
    j = re.match(pattern, email)
    lflag = True
    if (j):
        pass
    if lflag:
        if j:
            customer.execute(f'''Update Registration SET Email='{(email)}' where  Customer_id={condition}''')
            con.commit()
            # return jsonify({'message': "Updation Sucess", "Status": 200})
        else:
            return jsonify(
                {"errors": "Invalid Credentials Email should be in this format(example@anything.com)", "Status": 201})

    if not lflag:
        return jsonify({"errors": "email Id already exists Kindly Change the email", "Status": 201})

    # password

    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,12}$'
    print(type(password),"hello")
    if (re.match(pattern,password)):
        customer.execute(f'''Update Registration SET Password='{password}' where  Customer_id={condition}''')
        con.commit()
        # return jsonify({'message': "Updation Sucess", "Status": 200})
    if not (re.match(pattern, password)):
        return jsonify({"errors": "Password does not meet the Creterias", "Status": 201})
    # address
    if (len(address) > 100):
        return jsonify({"errors": "Invalid Credentials Cannot Update the Address", "Status": 201})
    elif (address):
        customer.execute(f'''Update Registration SET Address='{address}' where Customer_id={condition}''')
        con.commit()
        # return jsonify({'message': "Updation Sucess", "Status": 200})
    if len(address) == 0:
        return jsonify({"errors": "Address Cannot Be Blank", 'Status': 201})
    # contact
    pattern = r'^[0-9]\d{9}$'
    if re.match(pattern, phone):
        customer.execute(f'''Update Registration SET Contact_Number='{phone}' where  Customer_id={condition}''')
        con.commit()
        return jsonify({'message': "Updation Success", "Status": 200})

    if not re.match(pattern, phone):
        return jsonify({"errors": "Cannot Update the Contact Number", "Status": 201})

@app.route('/remove-customer', methods=["POST"])
def removeCustomer():
    print('hi')
    cid=request.json.get('id')
    customer.execute("Delete from Registration Where Customer_Id=%s",(cid,))
    con.commit()
    return  jsonify({"message":"User Deleted Successfully","Status":200})
    
    
@app.route('/display_details', methods=["POST"])
def display_customer():
    cid=request.json.get("id")
    session['admincustid']=cid
    customer.execute('Select * from Registration where Customer_id =%s',(cid,))
    a=customer.fetchone()
    #print(a)
    if a==None:
        return jsonify({"message":"No Customer Found","Status":201})
    elif a!=None:
        return  jsonify({"name":a[0],"email":a[1],'address':a[3],"contact":a[4],"Status":200,"message":"Customer Found"})
    

@app.route('/display_custid', methods=["POST"])
def display_customer_id():
    cid=request.json.get("id")
    customer.execute('Select * from Registration where Customer_id =%s',(cid,))
    a=customer.fetchone()
    #print(a)
    if a==None:
        return jsonify({"message":"No Customer Found","Status":201})
    elif a!=None:
        return  jsonify({"name":a[0],"email":a[1],'address':a[3],"contact":a[4],"Status":200,"message":"Customer Found"})


@app.route('/display_prodid', methods=["POST"])
def display_product_id():
    cid = request.json.get("id")
    customer.execute('Select * from Products where Product_ID =%s', (cid,))
    a = customer.fetchone()
    print(a)
    if a == None:
        return jsonify({"message": "No Product Found", "Status": 201})
    elif a != None:
        return jsonify(
            {"name": a[0], "email": a[1], 'address': a[3], 'desc': a[2], "contact": a[4], "Status": 200,
             "message": "Customer Found"})


@app.route('/display_custname', methods=["POST"])
def display_customer_name():
    cid=request.json.get("id")
    customer.execute(f'''select * from Registration where Customer_Name Like %s''',('%' + cid + '%',))
    a=customer.fetchall()
    if a == []:
        return jsonify({"message": "No Customer Found", "Status": 201})
    elif a != []:
        return jsonify({"values": a, "Status": 200, "message": "Customer Found"})

@app.route('/display_prodname', methods=["POST"])
def display_product_name():
    cid = request.json.get("id")
    customer.execute(f'''select * from Products where Product_name Like %s''', ('%' + cid + '%',))
    a = customer.fetchall()
    print(a)
    if a == []:
        return jsonify({"message": "No Product Found", "Status": 201})
    elif a != []:
        return jsonify(
            {"values" : a, "Status": 200, "message": "Customer Found"})




@app.route('/display_mails', methods=["POST"])
def display_customer_emails():
    domain = request.json.get('id')
    customer.execute(f'''select * from Registration where Email like %s ''',('%'+domain+'%',))
    a=customer.fetchall()
    print(domain)
    if a==[]:
        return jsonify({"message":"No Customer Found","Status":201})
    elif a!=[]:
        return jsonify({"values":a,"Status":200,"message":"Customer Found"})
    
    
@app.route('/display_category', methods=["POST"])
def display_prod_category():
    domain = request.json.get('id')
    customer.execute(f'''select * from Products where Description like %s ''', ('%' + domain + '%',))
    a = customer.fetchall()
    print(domain)
    if a == []:
        return jsonify({"message": "No Product Found", "Status": 201})
    elif a != []:
        return jsonify({"values": a, "Status": 200, "message": "Product Found"})


    

@app.route('/searchcust')
@admin_login_required
def sort():
    return render_template('admin_customersearch.html')

    
@app.route("/admin_custstatus")
@admin_login_required
def status_check():
    customer.execute( '''SELECT * FROM Registration''')
    a=customer.fetchall()
    return render_template( 'admin_custstatus.html',ta=a)  

@app.route('/butonstscheck',methods=['POST']) 
def butoncheck():
    custid=request.json.get('id')
    customer.execute('select Status from Registration where Customer_id=%s',(custid,)) 
    b=customer.fetchone()
    
    if b[0]=="Active":
        customer.execute('UPDATE Registration SET Status="Inactive" WHERE Customer_id=%s ', (custid,))
        con.commit()
        print("hey")
        return jsonify({"status":"Inactive"})
    
    if b[0]=="Inactive":
        customer.execute('UPDATE Registration SET Status="Active" WHERE Customer_id=%s ', (custid,))
        con.commit()
        return jsonify({"status":"Active"})


@app.route('/add-prod',methods=["POST"])
def add_product():
    print("add product request recieved")
    print("JSON Value",request.json)
    if request.method == "POST":
        product_id = request.json.get("pid")
        product_name = request.json.get("pname")
        product_desc = request.json.get("desc")
        product_quant = request.json.get("quant")
        product_price = request.json.get("price")

    customer.execute('''select * from Products where Product_ID =%s''', (product_id,))
    r = customer.fetchall()
    if (r != ()):
        _message = "Product already added"
        _status = "invalid"
    else:
        customer.execute(
            '''Insert Into Products(Product_ID,Product_Name,Description,Quantity,Price) values(%s, %s, %s, %s, %s)''',
            (product_id, product_name, product_desc, product_quant, product_price))
        con.commit()

        _message = "Product added Successfully"
        _status = "valid"

    return jsonify({"name": product_name, "customer": product_id, "status": _status,
                    "message": _message})


@app.route('/update-product',methods=["POST"])
def update_product():
    print("update product request recieved")
    print("JSON Value",request.json)
    if request.method == "POST":
        product_id = int(request.json.get("pid"))
        product_name = request.json.get("pname")
        product_desc = request.json.get("desc")
        product_quant = request.json.get("quant")
        product_price = request.json.get("price")

        customer.execute('''Update Products SET Product_Name =%s,Description =%s,Quantity =%s,Price =%s Where Product_ID =%s''', ( product_name, product_desc, product_quant, product_price,product_id))
        con.commit()

    _message = "Product added Successfully"
    _status = "valid"

    return jsonify({"name": product_name, "customer": product_id, "status": _status,
                    "message": _message})

@app.route('/delete-prod',methods=["POST"])
def delete_product():
    print("delete product request recieved")
    print("JSON Value",request.json)
    if request.method == "POST":
        product_id = request.json.get("pid")

    customer.execute('''select * from Products where Product_ID =%s''', (product_id,))
    r = customer.fetchall()
    if r == []:
        _message = "Product Not available"
        _status = "invalid"
    else:
        customer.execute('''Delete from Products where Product_ID =%s''', (product_id,))
        con.commit()

        _message = "Product deleted Successfully"
        _status = "valid"

    return jsonify({"product_id": product_id, "status": _status,
                    "message": _message})


@app.route('/search-prod',methods=["GET"])
def serach_admin_product():
    print("search product request recieved")
    print("JSON Value",request.json)
    if request.method == "GET":
        product_id = request.json.get("pid")

    customer.execute('''select * from Products where Product_ID =%s''', (product_id,))
    r = customer.fetchall()
    if r == []:
        _message = "Product Not available"
        _status = "invalid"
        _details = 'null'
    else:
        print(list(r))
        _message = "Product added Successfully"
        _status = "valid"

    return jsonify({"product_id": product_id, "status": _status,
                    "message": _message})
    

@app.route('/admin-add-product')
@admin_login_required
def admin_add_product():
    return render_template('admin_addproduct.html')

@app.route('/admin-update-product')
@admin_login_required
def admin_update_product():
    value = session['adminprodid']
    customer.execute(f'''select * from Products where Product_ID =%s''', (value,))
    r = customer.fetchone()
    print(r)
    return render_template('ogc_updateproduct.html',pid=r[0], pname=r[1], desc=r[2], quan=r[3], price=r[4])



@app.route('/rendersort')
@admin_login_required
def rendersorting():
    customer.execute("select * from Products")
    r=customer.fetchall()
    return render_template("sort.html",ta=r)

@app.route('/sortproduct',methods=['POST'])
def sortingProduct():
    funtiopass = request.json.get("fun")
    print(funtiopass)
    if funtiopass == 'quan':
        customer.execute("Select * from Products Order By Quantity")
        r=customer.fetchall()
        print(r)
        return jsonify({"Status":200,"values":r})
    
    elif funtiopass == 'price':
        customer.execute("Select * from Products Order By Price")
        r = customer.fetchall()
        print(r)
        return jsonify({"Status":200,"values":r})
    
@app.route('/redersearch',methods=['POST'])   
def searching():
    value=request.json.get('search')
    print(value)
    customer.execute('Select * from Products where Product_Name like %s ',( value + '%',))
    r=customer.fetchall()
    print(r)
    keys_list = ['id', 'name', 'desc', 'quant', 'price']
    temp_dict = {}
    res_list = []
    lis = []
    for each in r:
        res_list.append(list(each))

    for val in res_list:
        temp_dict = dict(zip(keys_list,val))
        lis.append(temp_dict)

    return jsonify({'products' : lis})

@app.route('/customerinactive')

def customerinactive():
    value=session['custid']
    print(value)
    customer.execute(f'''update Registration set Status='Inactive' where Customer_id=%s ''',(value,))
    con.commit()
    session.pop("custid",None)
    return render_template('ogc_login.html')

@app.route("/prdsearch",methods=['POST'])
def prdsearch():
    value=request.json.get("search")
    print(value)
    customer.execute('Select * from Products where Product_Name like %s ',( value + '%',))
    r=customer.fetchall()
    return jsonify({
        "Status":200,
        "values":r
    })
    
    
   
   
@app.route("/admn-validate",methods=['POST'])   
def admvalidate():
    print(session.items())
    adminid=request.json.get("adminid")
    password=request.json.get("password")
    session['admincustid']=adminid
    session['password']=password
    print(adminid,password)
    customer.execute('select Admin_Id,Password from Admin where Admin_Id=%s and Password=%s',(adminid,password,))
    adminget=customer.fetchone()
    if adminget is None:
        return jsonify({"status":201,"message":"Invalid Credentials"})
    else:
        if password == adminget[1]:
            return jsonify({"status":200,"message":"Logged In Successfully"})
        else:
            return jsonify({"status":201,"message":"Invalid Password"}) 
    
   

   
@app.route('/adminprof')
@admin_login_required
def adminprof():
    id=session['admincustid']
    print(id)
    customer.execute('select * from Admin where Admin_Id=%s',(id,))
    adminget=customer.fetchone()
    print(adminget)
    return render_template("adminprofile.html",name=adminget[1],contact=adminget[3])  

@app.route('/admin-profile')
@admin_login_required
def rederupdate():
    id=session['admincustid']
    customer.execute('select * from Admin where Admin_Id=%s',(id,))
    adminget=customer.fetchone()
    return  render_template("adminupdation.html",name=adminget[1],contact=adminget[3])

@app.route('/admin-profile-updates'  , methods = ['POST'])
def Admin_profile_update():
    updatede=request.json.get('name')
    contact=request.json.get('contact')
    value = session['admincustid']
    customer.execute(f'''Update Admin SET Admin_Name='{updatede}',Contact_Number={contact} where Admin_ID={value}''')
    con.commit()
    return jsonify({'message': "Updation Success", "Status": 200})

     
@app.route("/Contact")
def inactivelander():
    return render_template('lander.html')
 
@ app.route("/resttoactivate")
def activate():
    value=session['custid']
    customer.execute(f'''update Registration set Status='Active' where Customer_id=%s ''',(value,))
    con.commit()
    return render_template('ogc_login.html')
      
@app.route('/admin-update-prodmain')
@admin_login_required
def admin_update_product_main():
    
    return render_template('admin_product_update.html')

@app.route('/admin-delete-product')
@admin_login_required
def admin_remove_product():
    return render_template('admin_remove_product.html')

@app.route('/admin-search-product')
@admin_login_required
def admin_search_product():
    return render_template('admin_productsearch.html')

@app.route('/admin-login')
def admin_login():
    return render_template('admin_login.html')

@app.route("/admin-register")
def admin_register():
    return render_template('admin_register.html')

@app.route('/adminregister-validate',methods=["POST"])
def adminregisterValidate():
    if request.method == "POST":
        name = request.json.get("userName")
        pwd = request.json.get("userPassword")
        cid = request.json.get("customerId")
        contact = request.json.get("usernumber")
    res = adminnewregister(name, pwd,contact, cid)
    print(res)
    print(f"UID - {cid} \nPassword - {pwd}")
    return jsonify(res)


def adminnewregister(name, password, contact_no, c_id):
    customer.execute('''Insert Into Admin values(%s, %s, %s, %s)''', (c_id,name,password,contact_no))
    con.commit()
    return {"customer" : c_id ,"status" : 'valid',"message" : "Admin Registration Successful"}

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

    
if __name__ == "__main__":
    app.run(debug=True)
