# from flask import Flask,render_template,request
# import pymysql

# def sql_connection():
#     conn=pymysql.connect(user='root',password='wimtez-guqBat-nicca5',db='MINI_DATABASE',host='localhost',port=3306, autocommit=True)
#     c=conn.cursor()
#     return conn, c

# app = Flask(__name__)
# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/add_lawyer',methods=['GET','POST'])
# def add_lawyer():
#     if request.method == 'POST':
#         lid = request.form.get('lid')
#         lname= request.form.get('lname')
#         ltype=request.form.get('ltype')
#         lphone=request.form.get('lphone')
#         laddress=request.form.get('laddress')
       
#         conn,c = sql_connection()
#         c.execute("INSERT INTO lawyer VALUES ('{}','{}','{}',{},'{}')".format(lid,lname,ltype,int(lphone),laddress))   
#         conn.commit()
#         conn.close()
#         c.close()
#     return render_template('lawyer/add.html')


# @app.route('/display_lawyers', methods=['GET'])
# def display_lawyers():
#     filter_lawyer_type = request.args.get('filter_lawyer_type', '')
#     search_lawyer_name = request.args.get('search_lawyer_name', '')

#     conn, c = sql_connection()

#     if filter_lawyer_type:
#         c.execute("SELECT * FROM lawyer WHERE ltype = %s", (filter_lawyer_type,))
#     elif search_lawyer_name:
#         c.execute("SELECT * FROM lawyer WHERE lname LIKE %s", ('%' + search_lawyer_name + '%',))
#     else:
#         c.execute("SELECT * FROM lawyer")

#     lawyers = c.fetchall()

#     conn.close()
#     c.close()

#     return render_template('lawyer/displaylawyer.html', lawyers=lawyers)


# @app.route('/add_client', methods=['GET', 'POST'])
# def add_client():
#     if request.method == 'POST':
#         lid = request.form.get('lid')
#         cid = request.form.get('cid')
#         cname= request.form.get('cname')
#         cphone=request.form.get('cphone')
#         caddress=request.form.get('caddress')
       
#         conn,c = sql_connection()
#         c.execute("INSERT INTO client VALUES ('{}','{}','{}',{},'{}')".format(lid,cid,cname,int(cphone),caddress))   
#         conn.commit()
#         conn.close()
#         c.close()
#     return render_template('client/add.html')
   
# if __name__=='__main__':
#     app.run(debug=True)
    
    
    
    
    
    
    





from flask import Flask, render_template, request,redirect,url_for
import mysql.connector

app = Flask(__name__)
authenticated_lawyer_id = None
# MySQL configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'wimtez-guqBat-nicca5',
    'database': 'MINI_DATABASE',
    'autocommit': True
}

def sql_connection():
    conn = mysql.connector.connect(**db_config)
    c = conn.cursor(buffered=True)
    return conn, c

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_lawyer', methods=['GET', 'POST'])
def add_lawyer():
    if request.method == 'POST':
        lid = request.form.get('lid')
        lname = request.form.get('lname')
        ltype = request.form.get('ltype')
        lphone = request.form.get('lphone')
        laddress = request.form.get('laddress')

        conn, c = sql_connection()
        c.execute("INSERT INTO lawyer VALUES (%s, %s, %s, %s, %s)",
                  (lid, lname, ltype, int(lphone), laddress))
        conn.close()
        c.close()

    return render_template('lawyer/add.html')

@app.route('/display_lawyers', methods=['GET'])
def display_lawyers():
    filter_lawyer_type = request.args.get('filter_lawyer_type', '')
    search_lawyer_name = request.args.get('search_lawyer_name', '')

    conn, c = sql_connection()

    if filter_lawyer_type:
        c.execute("SELECT * FROM lawyer WHERE ltype = %s", (filter_lawyer_type,))
    elif search_lawyer_name:
        c.execute("SELECT * FROM lawyer WHERE lname LIKE %s", ('%' + search_lawyer_name + '%',))
    else:
        c.execute("SELECT * FROM lawyer")

    lawyers = c.fetchall()

    conn.close()
    c.close()

    return render_template('lawyer/displaylawyer.html', lawyers=lawyers)

@app.route('/lawyer_login', methods=['GET', 'POST'])
def lawyer_login():
    global authenticated_lawyer_id

    if request.method == 'POST':
        lid = request.form.get('lid')
        lname = request.form.get('lname')

        # Check the credentials against your database
        conn, c = sql_connection()
        c.execute("SELECT * FROM lawyer WHERE lid = %s AND lname = %s", (lid, lname))
        lawyer = c.fetchone()
        conn.close()
        c.close()

        if lawyer:
            # Authentication successful, store lawyer ID in the global variable
            authenticated_lawyer_id = lawyer[0]
            return redirect(url_for('display_clients'))

        # Authentication failed, show an error message or redirect to login page
        error_message = "Invalid credentials. Please try again."
        return render_template('lawyer/lawyerlogin.html', error_message=error_message)

    return render_template('lawyer/lawyerlogin.html')


@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        lid = request.form.get('lid')
        cid = request.form.get('cid')
        cname = request.form.get('cname')
        cphone = request.form.get('cphone')
        caddress = request.form.get('caddress')

        conn, c = sql_connection()
        c.execute("INSERT INTO client VALUES (%s, %s, %s, %s, %s)",
                  (cid, lid, cname, int(cphone), caddress))
        conn.close()
        c.close()

    return render_template('client/add.html')



@app.route('/display_clients', methods=['GET'])
def display_clients():
    filter_client_name = request.args.get('filter_client_name', '')

    conn, c = sql_connection()

    if filter_client_name:
        c.execute("SELECT * FROM client WHERE cname LIKE %s", ('%' + filter_client_name + '%',))
    else:
        c.execute("SELECT * FROM client")

    clients = c.fetchall()

    conn.close()
    c.close()

    return render_template('client/displayclient.html', clients=clients)

if __name__ == '__main__':
    app.run(debug=True)

    
    
    