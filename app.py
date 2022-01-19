import csv
import os
from flask import render_template, request, Flask, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from config import password


def set_up_db():
    URL = "mongodb+srv://RogueMongoDB:"+password+"@cluster0.b6ljn.mongodb.net/sample_supplies?retryWrites=true&w=majority"

    # connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
    client = MongoClient(URL)
    db = client.Inventory
    return db



# mongo = PyMongo(app)
app = Flask(__name__)
db = set_up_db()


#Add item 
@app.route('/add_item', methods=['POST', 'GET'])
def add_item():
    if request.method == 'GET':
        return f"The URL /data is accessed directly."
    if request.method == 'POST':
        form_data = request.form
        new_item = {}
        #gather form data
        for i in form_data:
            if 'name' in i:
                new_item['name'] = form_data[i]
            elif 'description' in i:
                new_item['description'] = form_data[i]
            elif 'count' in i:
                new_item['count'] = int(form_data[i])
            else:
                print("add error")
        new_item['deleted'] = 0
        print(new_item)
        #add new item into the database
        db.Inventory.insert_one(new_item)
        return redirect(url_for('.hello'))

#Export to csv
@app.route('/export_table', methods=['POST', 'GET'])
def export_table():
    if request.method == 'GET':
        return f"The URL /data is accessed directly." 
    if request.method == 'POST':
        fname=""
        form_data = request.form
        for i in form_data:
            if 'name' in i:
                fname = form_data[i]
        print("exporting table")
        print(fname)
        mongo_export_to_file(fname)
        return redirect(url_for('.hello'))
        
#Export to CSV
def mongo_export_to_file(fname):  
    # make an API call to the MongoDB server
    mongo_docs = db.Inventory.find({'deleted':0})

    fieldnames = list(mongo_docs[0].keys())
    fieldnames.remove('_id')
    fieldnames.remove('deleted')

    # join directories and output file in csv format
    output_dir = os.path.join('.', 'exports', '')
    print(output_dir)
    output_file = os.path.join(output_dir, fname+'.csv')
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(mongo_docs)
    return;

#Delete item 
@app.route('/delete_item', methods=['POST', 'GET'])
def delete_item():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        id = ""
        for i in form_data:
            if 'id' in i:
                id = form_data[i]
        #set deleted =1 for future functionality 
        db.Inventory.update_one({'_id': ObjectId(id)}, {
                                '$inc': {'deleted': 1}})

        return redirect(url_for('.hello'))

#user modify item
@app.route('/update_item', methods=['POST', 'GET'])
def update_item():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        new_item = {}
        id = ""
        #get data
        for i in form_data:
            if 'name' in i:
                new_item['name'] = form_data[i]
            elif 'description' in i:
                new_item['description'] = form_data[i]
            elif 'count' in i:
                new_item['count'] = int(form_data[i])
            elif 'id' in i:
                id = form_data[i]
            else:
                print("wrong")
                print(i)
        #replace old item with new one
        new_item['deleted'] = 0
        db.Inventory.replace_one({'_id': ObjectId(id)}, new_item)
        return redirect(url_for('.hello'))


#home page with data table on it
@app.route('/')
def hello():
    inv = db.Inventory.find({'deleted': 0})
    print(inv)
    data = []
    for i in inv:
        print(i)
        data.append(i)
    inv = [{"name": "hammer", "description": "a hammer", "count": 2}]*40

    return render_template('home.html', inv=data)


def main():
    app.run(host='localhost', port=5000, debug=True)
    db = set_up_db()
    print(db)
