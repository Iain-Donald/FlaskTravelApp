from email.policy import default
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

    def updateListingByID(id, newData):
        f = open('flask_app\controllers\db.json')
        data = json.load(f)
        listingData = "-1"
        for i in data['Listings']:
            print(i)
            if(int(i['id']) == id):
                listingData = i

        return -1

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

    def getAllUsers():
        f = open('flask_app\controllers\db.json')
        data = json.load(f)
        #Listings = "-1"
        Users = data['Users']

    def deleteListingByID(ID):
        ###f = open('flask_app\controllers\db.json')
        ###data = json.load(f)

        with open("flask_app\controllers\db.json") as f:
            data = json.load(f)

        idx = 0

        for i in data['Listings']:
            print(i['id'] + "  ID: " + ID)
            if i['id'] == ID:
                print("TRUE")
                del data['Listings'][idx]
            idx += 1

        with open("flask_app\controllers\db.json", 'w', encoding='utf-8') as fa:
            fa.write(json.dumps(data, indent=4))

    def deleteUserByID():
        return -1
            
        return Users
    