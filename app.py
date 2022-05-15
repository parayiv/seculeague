from flask import Flask, render_template, redirect, request, flash, jsonify, flash, url_for, session
from models import app, db, qradar, Seculeague, News, History, QrMinusSl, SlMinusQr, Rmvd
#from flask_mysqldb import MySQL,MySQLdb #pip install flask-mysqldb https://github.com/alexferl/flask-mysqldb
from sqlalchemy import delete
from datetime import datetime
import re
import secrets
import collections
from tools import qrminussl, slminusqr, pulldb, newsUpdateID, max_last_updated
from time import sleep

# index endpoint
@app.route('/home')
@app.route('/')
def index():
    d = collections.defaultdict(dict)
    #number of UC Qradar DB
    NQr = qradar.query.count()
    if NQr == 0:
        pulldb()
    NQr = qradar.query.count()
    NQrFlow = qradar.query.filter_by(TYPE='FLOW').count()
    NQrEvent = qradar.query.filter_by(TYPE='EVENT').count()
    NQrCom = qradar.query.filter_by(TYPE='COMMON').count()
    d['NQr']['Total'] = NQr
    d['NQr']['Flow'] = NQrFlow
    d['NQr']['Event'] = NQrEvent
    d['NQr']['Common'] = NQrCom

    #number of UC Seculeague
    NSe = Seculeague.query.count()
    NSeFlow = Seculeague.query.filter_by(TYPE='FLOW').count()
    NSeEvent = Seculeague.query.filter_by(TYPE='EVENT').count()
    NSeCom = Seculeague.query.filter_by(TYPE='COMMON').count()
    d['NSe']['Total'] = NQr
    d['NSe']['Flow'] = NQrFlow
    d['NSe']['Event'] = NQrEvent
    d['NSe']['Common'] = NSeCom
    #number of UC News
    NNe = News.query.count()
    NNeFlow = News.query.filter_by(TYPE='FLOW').count()
    NNeEvent = News.query.filter_by(TYPE='EVENT').count()
    NNeCom = News.query.filter_by(TYPE='COMMON').count()
    d['NNe']['Total'] = NNe
    d['NNe']['Flow'] = NNeFlow
    d['NNe']['Event'] = NNeEvent
    d['NNe']['Common'] = NNeCom
    #number of UC Rmvd
    NRe = Rmvd.query.count()
    NReFlow = Rmvd.query.filter_by(TYPE='FLOW').count()
    NReEvent = Rmvd.query.filter_by(TYPE='EVENT').count()
    NReCom = Rmvd.query.filter_by(TYPE='COMMON').count()
    d['NRe']['Total'] = NRe
    d['NRe']['Flow'] = NReFlow
    d['NRe']['Event'] = NReEvent
    d['NRe']['Common'] = NReCom
    #number of UC QrMinusSl
    NQrsl = QrMinusSl.query.count()
    NQrslFlow = QrMinusSl.query.filter_by(TYPE='FLOW').count()
    NQrslEvent = QrMinusSl.query.filter_by(TYPE='EVENT').count()
    NQrslCom = QrMinusSl.query.filter_by(TYPE='COMMON').count()
    d['NQrsl']['Total'] = NQrsl
    d['NQrsl']['Flow'] = NQrslFlow
    d['NQrsl']['Event'] = NQrslEvent
    d['NQrsl']['Common'] = NQrslCom
    #number of UC SlMinusQr
    NSlqr = SlMinusQr.query.count()
    NSlqrFlow = SlMinusQr.query.filter_by(TYPE='FLOW').count()
    NSlqrEvent = SlMinusQr.query.filter_by(TYPE='EVENT').count()
    NSlqrCom = SlMinusQr.query.filter_by(TYPE='COMMON').count()
    d['NSlqr']['Total'] = NSlqr
    d['NSlqr']['Flow'] = NSlqrFlow
    d['NSlqr']['Event'] = NSlqrEvent
    d['NSlqr']['Common'] = NSlqrCom
    #number of UC History
    NHi = History.query.count()
    NHiFlow = History.query.filter_by(TYPE='FLOW').count()
    NHiEvent = History.query.filter_by(TYPE='EVENT').count()
    NHiCom = History.query.filter_by(TYPE='COMMON').count()
    d['NHi']['Total'] = NHi
    d['NHi']['Flow'] = NHiFlow
    d['NHi']['Event'] = NHiEvent
    d['NHi']['Common'] = NHiCom

    session['d'] = d

    return render_template('index.html', d=d)

# /qradar endpoint
@app.route('/qradar')
def qr():
    return render_template('qradar.html', v=max_last_updated) #send to the qradar page

@app.route('/qradar/api')
def qradr():
    return { 'data': [qr.to_dict() for qr in qradar.query]}

@app.route('/pull')
def pull():
    #session['d'] = d
    qp = session.get('d') # get the dictionary of Use cases of QRADAR
    
    return render_template('pull.html', qp=qp)

@app.route('/pulled')
def pulled():
    #pull the db from tools library file
    pulldb()

    qp = session.get('d')
    qpull = collections.defaultdict(dict) #dict contains the data after pull
    
    #number of UC Qradar DB after pull; _ap: after pull
    NQr_ap = qradar.query.count()
    NQrFlow_ap = qradar.query.filter_by(TYPE='FLOW').count()
    NQrEvent_ap = qradar.query.filter_by(TYPE='EVENT').count()
    NQrChanged_ap = qradar.query.filter_by(last_updated=max_last_updated).count() # Number of New records or changed records
    
    qpull['NQr']['Total'] = NQr_ap
    qpull['NQr']['Flow'] = NQrFlow_ap
    qpull['NQr']['Event'] = NQrEvent_ap
    qpull['NQr']['Change'] = NQrChanged_ap

    print("____________", qp, qpull)

    return render_template('pulled.html', qp=qp, qpull=qpull)


#### History ####
@app.route('/history')
def his():
    return render_template('history.html')

@app.route('/history/api')
def hstory():
    return { 'data': [his.to_dict() for his in History.query]}



#### SECULEAGUE ####
@app.route('/seculeague')
def sec():
    return render_template('seculeague.html')

@app.route('/seculeague/api')
def seculeague():
    newsUpdateID()
    return { 'data': [sec.to_dict() for sec in Seculeague.query]}


#This is the index route where we are going to
#query on all our employee data
@app.route('/management')
def manage():
    #db_tables = db.engine.table_names()
    if 'query' in session:
        query = session.get('query')
        if query == 'News':
            all_data = News.query.all()
            print('=============', query)

        elif query == 'QrMinusSl':
            print("update QRMINUSSL OKI")
            all_data = QrMinusSl.query.all()
            print('=============', query)
        elif query == 'SlMinusQr':
            all_data = SlMinusQr.query.all()
            print('=============', query)
        elif query == 'Rmvd':
            all_data = Rmvd.query.all()
            print('=============', query)
        else:
            all_data = News.query.all()
            print('=============', query)
    else:
        query = 'News'
        all_data = News.query.all()
        print('=============', query)
        
    return render_template("management.html", all_data=all_data, query=query)

# About PAGE
@app.route('/about')
def about():
    return render_template('about.html')


@app.route("/fetchrecords",methods=["POST","GET"])
def fetchrecords():
    if request.method == 'POST':
        query = request.form['query']
        session['query'] = query
        #print('_________query from seculeague________', session.get('q'))
        if query == 'News':
            all_data = News.query.all()
            print('News')
        elif query == 'QrMinusSl':
            qrminussl()
            all_data = QrMinusSl.query.all()
            print('QrMinusSl')
        elif query == 'SlMinusQr':
            slminusqr()
            all_data = SlMinusQr.query.all()
            print('SlMinusQr')
        elif query == 'Rmvd':
            all_data = Rmvd.query.all()
            print('Rmvd')
        else:
            search_text = request.form['query']
            print(search_text)
            all_data = News.query.all()

    return jsonify({'htmlresponse': render_template('response.html', all_data=all_data, query=query)})

#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():
    session['query'] = 'News'
    #print('_________query from seculeague________', session.get('q'))
    if request.method == 'POST':
        qr_id = secrets.token_hex(3)
        sl_id = secrets.token_hex(3)
        name = request.form['name']
        TYPE = request.form['type']
        enabled = request.form['enabled']
        comment = request.form['comment']
        owner = 'admin'
        identifier = 'NOT YET'
        origin = 'SYSTEM'
        creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        modification_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = 'N'
        count = 0
        previous_tbl = 'NULL'
        current_tbl = 'News'


        my_data = News(qr_id=qr_id, sl_id=sl_id, name=name, TYPE=TYPE, enabled=enabled, owner=owner, identifier=identifier, origin=origin, status=status, count=count, comment=comment)
        db.session.add(my_data)
        db.session.commit()
        db.session.close()
        
        his = History(qr_id=qr_id, sl_id=sl_id, name=name, TYPE=TYPE, enabled=enabled, owner=owner, identifier=identifier, origin=origin, status=status, count=count, comment=comment, previous_tbl='News')
        db.session.add(his)
        db.session.commit()
        db.session.close()
        
        flash("Use Case Inserted Successfully In NEW  TABLE")

        return redirect(url_for('manage'))




@app.route("/update",methods=["POST","GET"])
def update():
        if request.method == 'POST':
            field = request.form['field'] 
            value = request.form['value']
            editid = request.form['id']
            query = request.form['query']
            
            if query == 'News':
                my_data = News.query.get(editid)
                if field == 'qr_id':
                    my_data.qr_id = value
                if field == 'name':
                    my_data.name = value
                if field == 'TYPE':
                    my_data.TYPE = value
                if field == 'creation_date':
                    my_data.creation_date = value
                if field == 'comment':
                    my_data.comment = value

                db.session.commit()
                db.session.close()

        return jsonify(success)

#This route is for deleting an entry
@app.route('/delete/<query>/', methods = ['GET', 'POST'])
def delete(query):
    id = re.findall(r'\d+', query)[0]
    string = re.sub(r'[^a-zA-Z]', '', query)

    if string =='News':
        my_data = News.query.get(id)
        records = News.query.filter_by(id=id).all()
        for record in records:
            r = {
                'id': record.id,
                'qr_id': record.qr_id,
                'sl_id': record.sl_id,
                'name': record.name,
                'TYPE': record.TYPE,
                'enabled': record.enabled,
                'owner': record.owner,
                'identifier': record.identifier,
                'origin': record.origin,
                'creation_date': record.creation_date,
                'modification_date': record.modification_date,
                'deletion_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'status': 'D',
                'count': 2,
                'comment': record.comment,
                'previous_tbl': 'News'
            }
        print('-------------')

        #add to History for tracking
        his = History(qr_id=r['qr_id'], sl_id=r['sl_id'], name=r['name'], TYPE=r['TYPE'], enabled=r['enabled'], owner=r['owner'], identifier=r['identifier'], origin=r['origin'], 
                        creation_date=r['creation_date'], modification_date=r['modification_date'], status=r['status'], count=r['count'], comment=r['comment'], previous_tbl=r['previous_tbl'])
        db.session.add(his)
        db.session.commit()
        db.session.close()
        #add to Rmvd for tracking
        rmuc = Rmvd(qr_id=r['qr_id'], sl_id=r['sl_id'], name=r['name'], TYPE=r['TYPE'], enabled=r['enabled'], owner=r['owner'], identifier=r['identifier'], origin=r['origin'], 
                        creation_date=r['creation_date'], modification_date=r['modification_date'], status=r['status'], count=r['count'], comment=r['comment'], previous_tbl=r['previous_tbl'])
        db.session.add(rmuc)
        db.session.commit()
        db.session.close()
        #delete now
        my_data = News.query.get(id)
        db.session.delete(my_data)
        db.session.commit()
        db.session.close()

        flash("USE CASE Deleted Successfully FROM Added Table")

    elif string == 'Seculeague':
        my_data = Seculeague.query.get(id)
        records = Seculeague.query.filter_by(id=id).all()
        for record in records:
            r = {
                'id': record.id,
                'qr_id': record.qr_id,
                'sl_id': record.sl_id,
                'name': record.name,
                'TYPE': record.TYPE,
                'enabled': record.enabled,
                'owner': record.owner,
                'identifier': record.identifier,
                'origin': record.origin,
                'creation_date': record.creation_date,
                'modification_date': record.modification_date,
                'deletion_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'status': 'D',
                'count': 3,
                'comment': record.comment,
                'previous_tbl': 'Seculeague'
            }

        #add to History for tracking
        his = History(qr_id=r['qr_id'], sl_id=r['sl_id'], name=r['name'], TYPE=r['TYPE'], enabled=r['enabled'], owner=r['owner'], identifier=r['identifier'], origin=r['origin'], 
                        creation_date=r['creation_date'], modification_date=r['modification_date'], deletion_date=r['deletion_date'],status=r['status'], count=r['count'], comment=r['comment'], previous_tbl=r['previous_tbl'])
        db.session.add(his)
        db.session.commit()
        db.session.close()
        #add to Rmvd for tracking
        rmuc = Rmvd(qr_id=r['qr_id'], sl_id=r['sl_id'], name=r['name'], TYPE=r['TYPE'], enabled=r['enabled'], owner=r['owner'], identifier=r['identifier'], origin=r['origin'], 
                        creation_date=r['creation_date'], modification_date=r['modification_date'], deletion_date=r['deletion_date'],status=r['status'], count=r['count'], comment=r['comment'], previous_tbl=r['previous_tbl'])
        db.session.add(rmuc)
        db.session.commit()
        db.session.close()

        #delete now
        my_data = Seculeague.query.get(id)
        db.session.delete(my_data)
        db.session.commit()
        db.session.close()

        flash("USE CASE Deleted Successfully From Seculeague Table")

    elif string == 'QrMinusSl':
        my_data = QrMinusSl.query.get(id)
        records = QrMinusSl.query.filter_by(id=id).all()
        for record in records:
            r = {
                'id': record.id,
                'qr_id': record.qr_id,
                'sl_id': record.sl_id,
                'name': record.name,
                'TYPE': record.TYPE,
                'enabled': record.enabled,
                'owner': record.owner,
                'identifier': record.identifier,
                'origin': record.origin,
                'creation_date': record.creation_date,
                'modification_date': record.modification_date,
                'deletion_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'status': 'D',
                'count': 3,
                'comment': record.comment,
                'previous_tbl': 'QrMinusSl'
            }
        print(r)
        #add to History for tracking
        his = History(qr_id=r['qr_id'], sl_id=r['sl_id'], name=r['name'], TYPE=r['TYPE'], enabled=r['enabled'], owner=r['owner'], identifier=r['identifier'], origin=r['origin'], 
                        creation_date=r['creation_date'], modification_date=r['modification_date'], deletion_date=r['deletion_date'],status=r['status'], count=r['count'], comment=r['comment'], previous_tbl=r['previous_tbl'])
        db.session.add(his)
        db.session.commit()
        db.session.close()
        #add to Rmvd for tracking
        rmuc = Rmvd(qr_id=r['qr_id'], sl_id=r['sl_id'], name=r['name'], TYPE=r['TYPE'], enabled=r['enabled'], owner=r['owner'], identifier=r['identifier'], origin=r['origin'], 
                        creation_date=r['creation_date'], modification_date=r['modification_date'], deletion_date=r['deletion_date'],status=r['status'], count=r['count'], comment=r['comment'], previous_tbl=r['previous_tbl'])
        db.session.add(rmuc)
        db.session.commit()
        db.session.close()
        
        #delete now
        my_data = QrMinusSl.query.get(id)
        print("__________________________________________\n", id, string, my_data)
        #db.session.delete(my_data)
        #db.session.commit()
        #db.session.close()

        flash("USE CASE Deleted Successfully From TABLE: TO BE TESTED.")
    
    elif string == 'SlMinusQr':
        my_data = SlMinusQr.query.get(id)
        records = SlMinusQr.query.filter_by(id=id).all()
        for record in records:
            r = {
                'id': record.id,
                'qr_id': record.qr_id,
                'sl_id': record.sl_id,
                'name': record.name,
                'TYPE': record.TYPE,
                'enabled': record.enabled,
                'owner': record.owner,
                'identifier': record.identifier,
                'origin': record.origin,
                'creation_date': record.creation_date,
                'modification_date': record.modification_date,
                'deletion_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'status': 'D',
                'count': 3,
                'comment': record.comment,
                'previous_tbl': 'SlMinusQr'
            }

        #add to History for tracking
        his = History(qr_id=r['qr_id'], sl_id=r['sl_id'], name=r['name'], TYPE=r['TYPE'], enabled=r['enabled'], owner=r['owner'], identifier=r['identifier'], origin=r['origin'], 
                        creation_date=r['creation_date'], modification_date=r['modification_date'], deletion_date=r['deletion_date'],status=r['status'], count=r['count'], comment=r['comment'], previous_tbl=r['previous_tbl'])
        db.session.add(his)
        db.session.commit()
        db.session.close()
        #add to Rmvd for tracking
        rmuc = Rmvd(qr_id=r['qr_id'], sl_id=r['sl_id'], name=r['name'], TYPE=r['TYPE'], enabled=r['enabled'], owner=r['owner'], identifier=r['identifier'], origin=r['origin'], 
                        creation_date=r['creation_date'], modification_date=r['modification_date'], deletion_date=r['deletion_date'],status=r['status'], count=r['count'], comment=r['comment'], previous_tbl=r['previous_tbl'])
        db.session.add(rmuc)
        db.session.commit()
        db.session.close()
        
        #delete now
        my_data = SlMinusQr.query.get(id)
        #db.session.delete(my_data)
        #db.session.commit()
        #db.session.close()

        flash("USE CASE Deleted Successfully From 'TABLE: TO BE REVIEWED FROM EXTERNAL SOURCES.'")
    
    else:
        flash('ERROR: Unknown Action, Please Try again.')

    session['query'] = string
    return redirect(url_for('manage'))


# commit the USE CASE ; This means you add it to SECULEAGUE TABLE

#This route is for adding Row to SECULEAGUE TABLE
@app.route('/add/<query>/', methods = ['GET', 'POST'])
def add(query):
    id = re.findall(r'\d+', query)[0]
    string = re.sub(r'[^a-zA-Z]', '', query)

    if string =='News':
        my_data = News.query.get(id)
        records = News.query.filter_by(id=id).all()
        for record in records:
            r = {
                'id': record.id,
                'qr_id': record.qr_id,
                'sl_id': record.sl_id,
                'name': record.name,
                'TYPE': record.TYPE,
                'enabled': record.enabled,
                'owner': record.owner,
                'identifier': record.identifier,
                'origin': record.origin,
                'creation_date': record.creation_date,
                'modification_date': record.modification_date,
                'status': 'C',
                'count': 2,
                'comment': record.comment,
                'previous_tbl': 'News'
            }
        print('-------------')

        #add to SECULEAGUE TABLE
        slg = Seculeague(qr_id=r['qr_id'], sl_id=r['sl_id'], name=r['name'], TYPE=r['TYPE'], enabled=r['enabled'], owner=r['owner'], identifier=r['identifier'], origin=r['origin'], 
                        creation_date=r['creation_date'], modification_date=r['modification_date'], status=r['status'], count=r['count'], comment=r['comment'], previous_tbl=r['previous_tbl'])
        db.session.add(slg)
        db.session.commit()
        db.session.close()
        #add to History for tracking
        rmuc = History(qr_id=r['qr_id'], sl_id=r['sl_id'], name=r['name'], TYPE=r['TYPE'], enabled=r['enabled'], owner=r['owner'], identifier=r['identifier'], origin=r['origin'], 
                        creation_date=r['creation_date'], modification_date=r['modification_date'], status=r['status'], count=r['count'], comment=r['comment'], previous_tbl=r['previous_tbl'])
        db.session.add(rmuc)
        db.session.commit()
        db.session.close()
        #delete from NEW now
        my_data = News.query.get(id)
        db.session.delete(my_data)
        db.session.commit()
        flash("Entry COMMITED Successfully")
    elif string == 'QrMinusSl':
        my_data = QrMinusSl.query.get(id)
        db.session.delete(my_data)
        db.session.commit()
        flash("Entry COMMITED Successfully")
    elif string == 'SlMinusQr':
        my_data = SlMinusQr.query.get(id)
        db.session.delete(my_data)
        db.session.commit()
        flash("Entry COMMITED Successfully")
    else:
        flash('ERROR: Could NOT Commit Entry !')

    session['query'] = string
    return redirect(url_for('manage'))



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)