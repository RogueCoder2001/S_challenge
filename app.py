from typing_extensions import Required
from flask import render_template, request, Flask, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_pymongo import PyMongo


def set_up_db():
    URL = "mongodb+srv://RogueMongoDB:Roge2001@cluster0.b6ljn.mongodb.net/sample_supplies?retryWrites=true&w=majority"

    # connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
    client = MongoClient(URL)
    db = client.Inventory
    return db


# app.config["MONGO_URI"] = "mongodb+srv://RogueMongoDB:Roge2001@cluster0.b6ljn.mongodb.net/sample_supplies?retryWrites=true&w=majority"
# mongo = PyMongo(app)
app = Flask(__name__)
db = set_up_db()


@app.route('/add_item', methods=['POST', 'GET'])
def add_item():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        new_item = {}
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
        db.Inventory.insert_one(new_item)

        return redirect(url_for('.hello'))


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
        print(id)
        db.Inventory.update_one({'_id': ObjectId(id)}, {
                                '$inc': {'deleted': 1}})
        # db.reviews.update_one({'_id': store.get('_id')}, {'$inc': {
        #                            'rating': 1}})
        # return render_template('data.html', form_data=form_data)
        return redirect(url_for('.hello'))


@app.route('/update_item', methods=['POST', 'GET'])
def update_item():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        new_item = {}
        id = ""
        for i in form_data:
            print(i)
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
        new_item['deleted'] = 0
        db.Inventory.replace_one({'_id': ObjectId(id)}, new_item)
        return redirect(url_for('.hello'))

# a simple page that says hello


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
