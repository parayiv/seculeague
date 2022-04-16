from flask import Flask, render_template, redirect, request, flash, jsonify, flash, url_for
from models import app, db, qradar, seculeague, news, history, qr_minus_sl, sl_minus_qr, rmvd
#from flask_mysqldb import MySQL,MySQLdb #pip install flask-mysqldb https://github.com/alexferl/flask-mysqldb

@app.route('/home')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/qradar')
def qr():
    return render_template('qradar.html')

@app.route('/qradar/api')
def qradr():
    return { 'data': [qr.to_dict() for qr in qradar.query]}

    
#This is the index route where we are going to
#query on all our employee data
@app.route('/seculeague')
def sclgue():
    db_tables = db.engine.table_names()
    print(db_tables)
    all_data = seculeague.query.all()
    return render_template("seculeague.html", all_data=all_data, db_tables=db_tables)


@app.route("/fetchrecords",methods=["POST","GET"])
def fetchrecords():
    query = 'seculeague'
    if request.method == 'POST':
        query = request.form['query']
        #print(query)
        if query == '' or  query == 'seculeague':
             all_data = seculeague.query.all()
             print('Seculeague')
        elif query == 'news':
            all_data = news.query.all()
            print('News')
        elif query == 'qr_minus_sl':
            all_data = qr_minus_sl.query.all()
            print('Qr_minus_sl')
        elif query == 'sl_minus_qr':
            all_data = sl_minus_qr.query.all()
            print('Sl_minus_qr')
        elif query == 'history':
            all_data = history.query.all()
            print('History')
        elif query == 'rmvd':
            all_data = rmvd.query.all()
            print('Rmvd')
        else:
            search_text = request.form['query']
            print(search_text)
            all_data = qradar.query.all()


    return jsonify({'htmlresponse': render_template('response.html', all_data=all_data, query=query)})

#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        name = request.form['name']
        Type = request.form['type']
        enabled = request.form['enabled']
        owner = 'admin'
        identifier = 'SYSTEM'
        origin = 'SYS'
        creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        modification_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        my_data = newUC(name, Type, enabled, owner, identifier, origin, creation_date, modification_date)
        db.session.add(my_data)
        db.session.commit()

        flash("Use Case Inserted Successfully")

        return redirect(url_for('Index'))



#this is our update route where we are going to update our employee
@app.route('/update', methods = ['GET', 'POST'])
def update():

    if request.method == 'POST':
        my_data = newUC.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.Type = request.form['type']
        my_data.origin = request.form['origin']

        db.session.commit()
        flash("Entry Updated Successfully")

        return redirect(url_for('Index'))


#This route is for deleting our employee
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = newUC.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Entry Deleted Successfully")

    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)