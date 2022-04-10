from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
import secrets
import mysql.connector
from models import SECU, newUC, RULES, app, db



#app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


#This is the index route where we are going to
#query on all our employee data
@app.route('/')
def Index():
    db_tables = db.engine.table_names()
    all_data = newUC.query.all()
    return render_template("index.html", all_data=all_data, db_tables=db_tables)


@app.route("/fetchrecords",methods=["POST","GET"])
def fetchrecords():
    query = 'newUC'
    if request.method == 'POST':
        query = request.form['query']
        #print(query)
        if query == '' or  query == 'newUC':
             all_data = newUC.query.all()
             query == 'newUC'
        elif query == 'RULES':
            all_data = RULES.query.all()
            print('all list')
        elif query == 'SECU':
            all_data = SECU.query.all()
            print('secu')
        else:
            search_text = request.form['query']
            print(search_text)
            all_data = newUC.query.all()


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