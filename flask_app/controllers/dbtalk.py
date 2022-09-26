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

    def getAllListings():
        f = open('flask_app\controllers\db.json')
        data = json.load(f)
        #Listings = "-1"
        Listings = data['Listings']
            

        return Listings
    