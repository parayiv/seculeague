from flask import Flask, render_template, redirect, request, flash, jsonify, flash, url_for
from modls import app, db, qradar
#from flask_mysqldb import MySQL,MySQLdb #pip install flask-mysqldb https://github.com/alexferl/flask-mysqldb

@app.route('/')
def index():
    return render_template('qr.html')

@app.route('/qradar')
def qradr():
    return { 'data': [qr.to_dict() for qr in qradar.query]}
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

