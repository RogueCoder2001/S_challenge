from pymongo import MongoClient, collection
from random import randint
# pprint library is used to make the output look more pretty
from pprint import pprint

URL = "mongodb+srv://RogueMongoDB:Roge2001@cluster0.b6ljn.mongodb.net/sample_supplies?retryWrites=true&w=majority"

# connect to MongoDB, change the << MONGODB URL >> to reflect your own connection string
client = MongoClient(URL)
db = client.business

# how to create records


def create_example_collection(db):
    # Step 2: Create sample data
    names = ['Kitchen', 'Animal', 'State', 'Tastey', 'Big', 'City',
             'Fish', 'Pizza', 'Goat', 'Salty', 'Sandwich', 'Lazy', 'Fun']
    company_type = ['LLC', 'Inc', 'Company', 'Corporation']
    company_cuisine = ['Pizza', 'Bar Food', 'Fast Food',
                       'Italian', 'Mexican', 'American', 'Sushi Bar', 'Vegetarian']
    for x in range(1, 501):
        business = {
            'name': names[randint(0, (len(names)-1))] + ' ' + names[randint(0, (len(names)-1))] + ' ' + company_type[randint(0, (len(company_type)-1))],
            'rating': randint(1, 5),
            'cuisine': company_cuisine[randint(0, (len(company_cuisine)-1))]
        }
        # Step 3: Insert business object directly into MongoDB via insert_one
        result = db.reviews.insert_one(business)
        # Step 4: Print to the console the ObjectID of the new document
        print('Created {0} of 500 as {1}'.format(x, result.inserted_id))
    # Step 5: Tell us that you are done
    print('finished creating 500 business reviews')


# how to find certain records
def find_five_star(db):
    fiveStar = db.reviews.find({'rating': 5})
    for i in fiveStar:
        print(i)


find_five_star(db)

# Updating records


def update(db, name):
    store = db.reviews.find_one({'name': name})
    print(int(store.get('rating')))
    result = db.reviews.update_one({'_id': store.get('_id')}, {'$inc': {
                                   'rating': 1}})
    print(result)
    pprint(db.reviews.find_one({'name': name}))


update(db, "Fish Pizza Corporation")
