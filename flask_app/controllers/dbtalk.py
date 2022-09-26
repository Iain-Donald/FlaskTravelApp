import json
from turtle import title
class dbtalk:
    def getListingByID(id):
        f = open('flask_app\controllers\db.json')
        data = json.load(f)
        listingData = "-1"
        for i in data['Listings']:
            print(i)
            if(int(i['id']) == id):
                listingData = i
            
        return listingData

    def getUserByID(id):
        f = open('flask_app\controllers\db.json')
        data = json.load(f)
        for i in data['Users']:
            print(i)
            if(int(i['userID']) == int(id)):
                return i
            
        return "User not found"

    def getUserByEmail(email):
        f = open('flask_app\controllers\db.json')
        data = json.load(f)
        userData = "-1"
        for i in data['Users']:
            print(i)
            if(i['email'] == email):
                userData = i
            
        return userData

    def getAllListings():
        f = open('flask_app\controllers\db.json')
        data = json.load(f)
        #Listings = "-1"
        Listings = data['Listings']
            
        return Listings
    