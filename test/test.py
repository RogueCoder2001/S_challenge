from pymongo import MongoClient
from random import randint
# pprint library is used to make the output look more pretty
from pprint import pprint
from bson.objectid import ObjectId
import csv
import os

URL = "mongodb+srv://RogueMongoDB:Roge2001@cluster0.b6ljn.mongodb.net/sample_supplies?retryWrites=true&w=majority"

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient(URL)
db = client.Inventory

#Same method as in app.py but with dummy data to conduct unit test
def add_item(form_data):
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
    #return redirect(url_for('.hello'))

def delete_item(form_data):
    # if request.method == 'GET':
    #     return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    # if request.method == 'POST':
        # form_data = request.form
        id = ""
        for i in form_data:
            if 'id' in i:
                id = form_data[i]
        #set deleted =1 for future functionality 
        db.Inventory.update_one({'_id': ObjectId(id)}, {
                                '$inc': {'deleted': 1}})

        #return redirect(url_for('.hello'))

#same method in app.py but put dummy data in for testing
def update_item(form_data):
    # if request.method == 'GET':
    #     return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    # if request.method == 'POST':
    #     form_data = request.form
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
        # return redirect(url_for('.hello'))

#Export to CSV
def mongo_export_to_file(fname):  
    # make an API call to the MongoDB server
    mongo_docs = db.Inventory.find({'deleted':0})

    fieldnames = list(mongo_docs[0].keys())
    fieldnames.remove('_id')
    fieldnames.remove('deleted')

    # join directories and output file in csv format
    output_dir = os.path.join('..', 'exports', '')
    print(output_dir)
    output_file = os.path.join(output_dir, fname+'.csv')
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(mongo_docs)
    return;


#create records
def create_example_collection():
    # Step 2: Create sample data
    names = ['Kitchen', 'Animal', 'State', 'Tastey', 'Big', 'City',
             'Fish', 'Pizza', 'Goat', 'Salty', 'Sandwich', 'Lazy', 'Fun']
    company_type = ['LLC', 'Inc', 'Company', 'Corporation']
    company_cuisine = ['Pizza', 'Bar Food', 'Fast Food',
                       'Italian', 'Mexican', 'American', 'Sushi Bar', 'Vegetarian']
    for x in range(1, 30):
        form_data = {
            'name': names[randint(0, (len(names)-1))] + ' ' + names[randint(0, (len(names)-1))] + ' ' + company_type[randint(0, (len(company_type)-1))],
            'description': company_cuisine[randint(0, (len(company_cuisine)-1))],
            'count': randint(1, 5)
        }
        # Step 3: Insert business object directly into MongoDB via insert_one
        add_item(form_data)
        # Step 4: Print to the console the ObjectID of the new document
    # Step 5: Tell us that you are done
    print('finished creating 500 business Inventory')


def main():
    #run unit test to create collection items
    create_example_collection()
    #view if records have entered
    inv=db.Inventory.find({'deleted': 0})
    for i in inv:
        print(i)
    
    #check update method
    store=db.Inventory.find_one({'deleted': 0})
    print("before updating")
    pprint(store)
    n_store={"id":store.get('_id'),"name":"new and improved store","description":"just a new store","count":60}
    update_item(n_store)
    print("After updating:")
    pprint(db.Inventory.find_one({'_id': store.get("_id")}))
    delete_item(n_store)
    print("After deleting:")
    pprint(db.Inventory.find_one({'_id': store.get("_id")}))
    #notice deleted now =1 and will not show on website
    
    #test export method
    mongo_export_to_file("testingtesting")
    
main()