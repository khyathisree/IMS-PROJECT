#Establish a connection to the SQL server
import sqlite3
from flask import Flask,jsonify,request,render_template
app=Flask(__name__)

conn=sqlite3.connect('ims.db')
cn=conn.cursor()

def idgenerator(tab): 
    conn = sqlite3.connect('ims.db')
    cur = conn.cursor()
    idval = ''
    if tab=='CUSTOMER':
        idval = 'CUST_ID'
    if tab=='PRODUCT':
        idval = 'PRODUCT_ID'
    if tab=='ORDERS':
        idval = 'ORDERS_ID'
    if tab=='SUPPLIER':
        idval = 'SUPPLIER_ID'
    print(tab,idval)
    cur.execute(f"SELECT {idval} FROM {tab}")
    new = cur.fetchall()
    cud = str(new[len(new)-1][0])
    for i in range(len(str(cud))):
        if cud[i].isnumeric():
            f = i
            break
    myint = cud[f:]
    myint = int(myint)+1
    return idval[0:3]+str(myint)




#cn.execute("insert into customer(cust_name,cust_addr,cust_mail) values('pqr','hyd','pqr@gmail.com')")
#conn.commit()

#cn.execute("Delete from customer where cust_id='cus10")
#conn.commit()

#-----

#customer_name='rtf'
##customer_addr='hyd'
#customer_email='rtf@gmail.com'

#cn.execute(f"insert into customer(cust_name,cust_addr,cust_mail) values('{customer_name}','{customer_addr}','{customer_email}')")
#conn.commit()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/show-customers')
def customer_show():
    conn=sqlite3.connect('ims.db')
    cn=conn.cursor()
    cn.execute("select * from customer")
    data=[]
    for i in cn.fetchall():
        customer={}
        customer['customer_id']=i[0]
        customer['customer_name']=i[1]
        customer['customer_addr']=i[2]
        customer['customer_email']=i[3]
        data.append(customer)

    return render_template('showcustomers.html',data=data)


@app.route('/show-product')
def product_show():
    conn=sqlite3.connect('ims.db')
    cn=conn.cursor()
    cn.execute("select * from product")
    data=[]
    for i in cn.fetchall():
        product={}
        product['product_id']=i[0]
        product['product_name']=i[1]
        product['stock']=i[2]
        product['price']=i[3]
        product['supplier_id']=i[4]
        data.append(product)

    return render_template('showproduct.html',data=data)



@app.route('/show-orders')
def orders_show():
    conn=sqlite3.connect('ims.db')
    cn=conn.cursor()
    cn.execute("select * from orders")
    data=[]
    for i in cn.fetchall():
        orders={}
        orders['orders_id']=i[0]
        orders['product_id']=i[1]
        orders['customer_id']=i[2]
        orders['quantity']=i[3]
        data.append(orders)

    return render_template('showorders.html',data=data)


@app.route('/show-supplier')
def supplier_show():
    conn=sqlite3.connect('ims.db')
    cn=conn.cursor()
    cn.execute("select * from supplier")
    data=[]
    for i in cn.fetchall():
        supplier={}
        supplier['supplier_id']=i[0]
        supplier['supplier_name']=i[1]
        supplier['supplier_addr']=i[2]
        supplier['supplier_email']=i[3]
        data.append(supplier)

    return render_template('showsupplier.html',data=data)



@app.route('/add-customer',methods=['GET','POST'])
def addcustomer():
    if request.method=='POST':
        conn=sqlite3.connect('ims.db')
        cn=conn.cursor()
        customer_name=request.form.get('name')   #from the addcustomers html file ID = "name"
        customer_addr=request.form.get('address')
        customer_mail=request.form.get('email')
        ID = idgenerator('CUSTOMER')
        cn.execute(f"insert into customer(cust_id,cust_name,cust_addr,cust_mail) values ('{ID}','{customer_name}','{customer_addr}','{customer_mail}')")
        conn.commit()
        print('Data has been inserted')
        return jsonify({'message':'successful'})
    else:
        return render_template('addcustomer.html')


@app.route('/update-customer',methods= ['GET','POST'])
def updatecustomer():
    if request.method== 'POST':
        conn = sqlite3.connect('ims.db')
        cn=conn.cursor()
        customer_id= request.form.get('customer_id')
        change= request.form.get('change')
        newvalue= request.form.get('newvalue')
        print(customer_id,change,newvalue)
        cn.execute(f"update customer set {change}='{newvalue}' where cust_id='{customer_id}'")
        conn.commit()
        print('data has been updated successfully!')
        return jsonify({'message':'successful'})
    else:
        return render_template('updatecustomer.html')



@app.route('/delete-customer',methods=['GET','POST'])
def deletecustomer():
    if request.method=='POST':
        conn = sqlite3.connect('ims.db')
        cn=conn.cursor()
        customer_id=request.form.get('customer_id')
        cn.execute(f"delete from customer where cust_id ='{customer_id}'")
        conn.commit()
        return jsonify({'message':'successful'})
    else:
        return render_template('deletecustomer.html')


@app.route('/add-product',methods=['GET','POST'])
def addproduct():
    if request.method=='POST':
        conn = sqlite3.connect('ims.db')
        cn=conn.cursor()
        product_name=request.form.get('product_name')
        stock=request.form.get('stock')
        price=request.form.get('price')
        supplier_id=request.form.get('supplier_id')
        ID = idgenerator('PRODUCT')
        cn.execute(f"insert into product(product_id,product_name,stock,price,supplier_id)values ('{ID}','{product_name}','{stock}','{price}','{supplier_id}')")
        conn.commit()
        print('Data has been inserted')
        return jsonify({'message':'successful'})
    else:
        return render_template('addproduct.html')


@app.route('/update-product',methods= ['GET','POST'])
def updateproduct():
    if request.method== 'POST':
        conn = sqlite3.connect('ims.db')
        cn=conn.cursor()
        product_id= request.form.get('product_id')
        change= request.form.get('change')
        newvalue= request.form.get('newvalue')
        print(product_id,change,newvalue)
        cn.execute(f"update product set {change}='{newvalue}' where product_id='{product_id}'")
        conn.commit()
        print('data has been updated successfully!')
        return jsonify({'message':'successful'})
    else:
        return render_template('updateproduct.html')



@app.route('/delete-product',methods=['GET','POST'])
def deleteproduct():
    if request.method=='POST':
        conn = sqlite3.connect('ims.db')
        cn=conn.cursor()
        product_id=request.form.get('product_id')
        cn.execute(f"delete from product where product_id ='{product_id}'")
        conn.commit()
        return jsonify({'message':'successful'})
    else:
        return render_template('deleteproduct.html')


@app.route('/add-supplier',methods=['GET','POST'])
def addsupplier():
    if request.method=='POST':
        conn = sqlite3.connect('ims.db')
        cn=conn.cursor()
        supplier_name=request.form.get('supplier_name')
        supplier_addr=request.form.get('supplier_addr')
        supplier_mail=request.form.get('supplier_mail')
        ID = idgenerator('SUPPLIER')
        cn.execute(f"insert into supplier(supplier_id,supplier_name,supplier_addr,supplier_mail) values ('{ID}','{supplier_name}','{supplier_addr}','{supplier_mail}')")
        conn.commit()
        print('Data has been inserted')
        return jsonify({'message':'successful'})
    else:
        return render_template('addsupplier.html')


@app.route('/update-supplier',methods= ['GET','POST'])
def updatesupplier():
    if request.method== 'POST':
        conn = sqlite3.connect('ims.db')
        cn=conn.cursor()
        supplier_id= request.form.get('supplier_id')
        change= request.form.get('change')
        newvalue= request.form.get('newvalue')
        print(supplier_id,change,newvalue)
        cn.execute(f"update supplier set {change}='{newvalue}' where supplier_id='{supplier_id}'")
        conn.commit()
        print('data has been updated successfully!')
        return jsonify({'message':'successful'})
    else:
        return render_template('updatesupplier.html')


@app.route('/delete-supplier',methods=['GET','POST'])
def deletesupplier():
    if request.method=='POST':
        conn = sqlite3.connect('ims.db')
        cn=conn.cursor()
        supplier_id=request.form.get('supplier_id')
        cn.execute(f"delete from supplier where supplier_id ='{supplier_id}'")
        conn.commit()
        return jsonify({'message':'successful'})
    else:
        return render_template('deletesupplier.html')


@app.route('/add-orders',methods=['GET','POST'])
def addorders():
    if request.method=='POST':
        conn = sqlite3.connect('ims.db')
        cn=conn.cursor()
        product_id=request.form.get('product_id')
        customer_id=request.form.get('customer_id')
        quantity=request.form.get('quantity')
        ID = idgenerator('ORDERS')
        cn.execute(f"insert into orders(orders_id,product_id,customer_id,quantity) values ('{ID}','{product_id}','{customer_id}','{quantity}')")
        conn.commit()
        print('Data has been inserted')
        return jsonify({'message':'successful'})
    else:
        return render_template('addorders.html')


@app.route('/update-orders',methods= ['GET','POST'])
def updateorders():
    if request.method== 'POST':
        conn = sqlite3.connect('ims.db')
        cn=conn.cursor()
        orders_id= request.form.get('orders_id')
        change= request.form.get('change')
        newvalue= request.form.get('newvalue')
        print(orders_id,change,newvalue)
        cn.execute(f"update orders set {change}='{newvalue}' where orders_id='{orders_id}'")
        conn.commit()
        print('data has been updated successfully!')
        return jsonify({'message':'successful'})
    else:
        return render_template('updateorders.html')


@app.route('/delete-orders',methods=['GET','POST'])
def deleteorders():
    if request.method=='POST':
        conn = sqlite3.connect('ims.db')
        cn=conn.cursor()
        orders_id=request.form.get('orders_id')
        cn.execute(f"delete from orders where orders_id ='{orders_id}'")
        conn.commit()
        return jsonify({'message':'successful'})
    else:
        return render_template('deleteorders.html')





    




if __name__=='__main__':
    app.run()


