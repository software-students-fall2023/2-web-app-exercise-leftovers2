from flask import Flask, render_template, request, redirect, url_for, make_response, session

import pymongo
from bson.objectid import ObjectId
from pymongo import MongoClient
import os
from db import db

contactList = db[os.getenv('MONGODB_COLLECTION')]

app = Flask(__name__)

## Main Page with a list of all contacts
@app.route('/')
def home():
    # return render_template('/index.html', flask_test='This test is a success!')
    return redirect(url_for('list_view'))

@app.route('/list_view', methods=['GET'])
def list_view():
    listing = contactList.find({})
    # session['listing'] = listing;
    return render_template('list_view.html', contacts=listing)

@app.route('/get_individual', methods=['POST'])
def get_individual():
    # return redirect(url_for('individual_view'))
    id = request.form.get('_id')
    contact = contactList.find_one({'_id':id})
    if contact:
        # session['current_contact'] = contact
        return redirect(url_for('individual_view', contact=contact))

## Individual Contact View
@app.route('/individual_view', methods=['GET'])
def individual_view():
    # contact = session['current_contact']
    contact = None
    return render_template('individual_view.html', contact=contact)
## Add Contact View
@app.route('/add_view', methods=['GET'])
def add_view():
    return render_template('add_view.html')

@app.route('/add_contact', methods=['POST'])
def add_contact():
    contact_name = request.form.get('fName')
    phone_number = request.form.get('fPhone')
    email = request.form.get('fEmail')
    home_address = request.form.get('fAddress')
    notes = request.form.get('fNotes')
    newContact = {'name':contact_name, 'phone':phone_number, 'email':email, 'address':home_address, 'notes':notes}
    contactList.insert_one(newContact)
    return redirect(url_for('list_view'))

## Delete View
@app.route('/delete_view', methods=['GET'])
def delete_view():
    # if(session['listing'] == None):
    listing = contactList.find({})
        # session['listing'] = listing
    # else:
        # listing = session['listing']
    return render_template('delete_view.html', contacts=listing)

@app.route('/delete_action', methods=['POST'])
def delete_action():
    id = request.form.get('_id')
    contact = contactList.find_one({'_id': id})
    # listing = session['listing']
    if contact:
        contactList.delete_one(contact);
        listing = contactList.find({})
        # session['listing'] = listing
        return render_template('delete_view.html', contacts=listing)
    else:
        error = 'Could not find contact to delete.'
        listing = contactList.find({})
        return render_template('delete_view.html', contacts=listing, error=error)

if __name__ == "__main__":
    app.run(debug=True)