from flask import Flask, render_template, redirect, request, flash, jsonify, flash, url_for
from models import app, db, qradar
#from flask_mysqldb import MySQL,MySQLdb #pip install flask-mysqldb https://github.com/alexferl/flask-mysqldb

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/qradar')
def qr():
    return render_template('qradar.html')

@app.route('/qradar/api')
def qradr():
    return { 'data': [qr.to_dict() for qr in qradar.query]}

    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)











"""
@app.route("/ajax_add",methods=["POST","GET"])
def ajax_add():
    if request.method == 'POST':
        name = request.form['name']
        origin = request.form['origin']
        owner = request.form['owner']
        name = request.form['name']
        Type = 'NOTYPE'
        enabled = 'NOT DEFIN'
        identifier = 'SYSTEM'
        creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        modification_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(name)
        
        if name == '':
            msg = 'Please Input name'  
        elif origin == '':
           msg = 'Please Input origin'  
        elif owner == '':
           msg = 'Please Input Full'  
        else:
            my_data = newUC(name, Type, enabled, owner, identifier, origin, creation_date, modification_date)       
            db.session.add(my_data)
            db.session.commit()      
            msg = 'New record created successfully'   
    return jsonify(msg)

 
@app.route("/ajax_update",methods=["POST","GET"])
def ajax_update():
    #cursor = mysql.connection.cursor()
    #cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        string = request.form['string']
        name = request.form['name']
        origin = request.form['origin']
        owner = request.form['owner']
        print(string)
 

        my_data = newUC.query.get(request.form.get('string'))

        my_data.name = request.form['name']
        my_data.origin = request.form['origin']
        my_data.owner = request.form['owner']

        db.session.commit()
        msg = 'Record successfully Updated' 
        #flash("Entry Updated Successfully")

    return jsonify(msg)  

@app.route("/ajax_update_sl",methods=["POST","GET"])
def ajax_update_sl():
    #cursor = mysql.connection.cursor()
    #cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        string = request.form['string']
        name = request.form['name']
        origin = request.form['origin']
        owner = request.form['owner']
        print(string)
 

        my_data = SECU.query.get(request.form.get('string'))

        my_data.name = request.form['name']
        my_data.origin = request.form['origin']
        my_data.owner = request.form['owner']

        db.session.commit()
        msg = 'Record successfully Updated' 
        #flash("Entry Updated Successfully")

    return jsonify(msg)   
 
@app.route("/ajax_delete",methods=["POST","GET"])
def ajax_delete():

    if request.method == 'POST':
        getid = request.form['string']
        ucase =  request.form['ucase']
        print(getid, ucase)
        
        if ucase == 'newUC':
            my_data = newUC.query.get(getid)
            db.session.delete(my_data)
            db.session.commit()
        
            #flash("Entry Deleted Successfully")
            msg = 'Record deleted successfully'
        else:
            #flash("Erroooor")
            msg = 'Could not delete entry'   
    return jsonify(msg) 
    #return redirect(url_for('ajax_delete'))


#delete seculeague entry
@app.route("/ajax_del_sl",methods=["POST","GET"])
def ajax_del_sl():

    if request.method == 'POST':
        getid = request.form['string'] 
        ucase =  request.form['ucase']
        print(getid, ucase)
        print('secu id:', getid)
        
        if ucase == 'SECU':
            my_data = SECU.query.get(getid)
            db.session.delete(my_data)
            db.session.commit()
        
            #flash("Entry Deleted Successfully")
            msg = 'Record deleted successfully'
        else:
            msg = 'Could not delete entry'
    return jsonify(msg) 


@app.route("/ajax_add_sl",methods=["POST","GET"])
def ajax_add_sl():
    if request.method == 'POST':
        name = request.form['name']
        origin = request.form['origin']
        owner = request.form['owner']
        name = request.form['name']
        TYPE = 'NOTYPE'
        enabled = 'NOT DEFIN'
        identifier = 'SYSTEM'
        creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        modification_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print('SECU', name)
        
        if name == '':
            msg = 'Please Input name'  
        elif origin == '':
           msg = 'Please Input origin'  
        elif owner == '':
           msg = 'Please Input Full'  
        else:
            my_data = SECU(name, TYPE, enabled, owner, identifier, origin, creation_date, modification_date)       
            db.session.add(my_data)
            db.session.commit()      
            msg = 'New record created successfully'   
    return jsonify(msg)

 
@app.route("/fetchrecords",methods=["POST","GET"])
def fetchrecords():
    if request.method == 'POST':
        query = request.form['query']
        #print(query)
        if query == '' or query == 'RULES':
            data = RULES.query.all()
            print('all list')
        elif query == 'SECU':
            data = SECU.query.all()
            print('SECU list')
            print("--------------")
            print(data)
        elif query == 'newUC':
            data = newUC.query.all()           
        else:
            search_text = request.form['query']
            print(search_text)
            data = SECU.query.all() 
    return jsonify({'htmlresponse': render_template('response.html', data=data)})
     
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)






@app.route('/qradar')
def qradar():
    perpage=10
    startat=page*perpage
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    result = cur.execute("SELECT * FROM qradar ORDER BY id limit %s, %s", (startat, perpage))
    data = list(cur.fetchall())

    return render_template('qradar.html', data=data, page=page)
"""