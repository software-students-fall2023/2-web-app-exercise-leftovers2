from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    make_response,
    session,
)

import pymongo
import re
from bson.objectid import ObjectId
from pymongo import MongoClient
import os
from db import db
from bson import json_util
import json


def parse_json(data):
    return json.loads(json_util.dumps(data))


contactList = db[os.getenv("MONGODB_COLLECTION")]

app = Flask(__name__)

app.secret_key = "very_secret_key_of_great_secrecy"


## Main Page with a list of all contacts
@app.route("/")
def home():
    # return render_template('/index.html', flask_test='This test is a success!')
    return redirect(url_for("list_view"))


@app.route("/list_view", methods=["GET"])
def list_view():
    listing = contactList.find({}).sort("name", 1)
    # session['listing'] = listing;
    return render_template("list_view.html", title="All Contacts", contacts=listing)


@app.route("/get_individual", methods=["POST"])
def get_individual():
    id = request.form.get("_id")
    contact = contactList.find_one({"_id": ObjectId(id)})
    if contact:
        session["current_contact"] = parse_json(contact)
        return redirect(url_for("individual_view", title="Contact", contact=contact))


## Individual Contact View
@app.route("/individual_view", methods=["GET"])
def individual_view():
    contact = session["current_contact"]
    return render_template("individual_view.html", title="Contact", contact=contact)


# Edit View and Edit Post
@app.route("/get_edits", methods=["POST"])
def get_edits():
    # new edits
    new_name = request.form.get("newName")
    new_phone = request.form.get("newPhone")
    new_email = request.form.get("newEmail")
    new_address = request.form.get("newAddress")
    new_notes = request.form.get("newNotes")

    id = request.form.get("_id")
    contact = contactList.find_one({"_id": ObjectId(id)})
    if contact:
        if new_name:
            contactList.update_one({"_id": ObjectId(id)}, {"$set": {"name": new_name}})
        if new_phone:
            contactList.update_one(
                {"_id": ObjectId(id)}, {"$set": {"phone": new_phone}}
            )
        if new_email:
            contactList.update_one(
                {"_id": ObjectId(id)}, {"$set": {"email": new_email}}
            )
        if new_address:
            contactList.update_one(
                {"_id": ObjectId(id)}, {"$set": {"address": new_address}}
            )
        if new_notes:
            contactList.update_one(
                {"_id": ObjectId(id)}, {"$set": {"notes": new_notes}}
            )

        # contact = session["current_contact"]
        return redirect(url_for("list_view"))


@app.route("/edit_view", methods=["GET"])
def edit_view():
    contact = session["current_contact"]
    return render_template("edit.html", title="Contact", contact=contact)


## Add Contact View
@app.route("/add_view", methods=["GET"])
def add_view():
    return render_template("add.html", title="Add Contact")


@app.route("/add_contact", methods=["POST"])
def add_contact():
    contact_name = request.form.get("fname")
    phone_number = request.form.get("fphone")
    email = request.form.get("femail")
    home_address = request.form.get("faddress")
    notes = request.form.get("fnotes")
    newContact = {
        "name": contact_name,
        "phone": phone_number,
        "email": email,
        "address": home_address,
        "notes": notes,
    }
    contactList.insert_one(newContact)
    return redirect(url_for("list_view"))


## Delete View
@app.route("/delete_view", methods=["GET"])
def delete_view():
    # if(session['listing'] == None):
    listing = contactList.find({}).sort("name", 1)
    # session['listing'] = listing
    # else:
    # listing = session['listing']
    return render_template("delete.html", title="Delete Contacts", contacts=listing)


@app.route("/delete_action", methods=["POST"])
def delete_action():
    id = request.form.get("_id")
    contact = contactList.find_one({"_id": ObjectId(id)})
    # listing = session['listing']
    if contact:
        contactList.delete_one(contact)
        listing = contactList.find({})
        # session['listing'] = listing
        return render_template("delete.html", title="Delete Contacts", contacts=listing)
    else:
        error = "Could not find contact to delete."
        print(error)
        # render_template('search.html', title="Search Contacts")
        listing = contactList.find({})
        return render_template(
            "delete.html", title="Delete Contacts", contacts=listing, error=error
        )


## Search View
@app.route("/search_view", methods=["GET"])
def search_view():
    return render_template("search.html", title="Search Contacts")

@app.route("/search_action", methods=["POST"])
def search_action():
    search_query = request.form.get("fsearch")
    # listing = contactList.find({ "name": search_query })
    regx = re.compile(search_query, re.IGNORECASE)
    # listing = contactList.find(
    #     { "name": { '$regex': regx}})
    
    listing = contactList.find({"$or": [
        { "name": { '$regex': regx}},
        { "phone": { '$regex': regx}},
        { "email": { '$regex': regx}},
        { "address": { '$regex': regx}},
        { "notes": { '$regex': regx}},
    ]})
    
    return render_template(
        "search_results.html", title="Search Results", query=search_query, length=len(list(listing.clone())), contacts=listing
    )


if __name__ == "__main__":
    app.run(debug=True)
