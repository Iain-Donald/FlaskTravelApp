from email.policy import default
import json
from turtle import title
class dbtalk:
    def getListingByID(id):
        f = open('flask_app\controllers\db.json')
        data = json.load(f)
        listingData = "-1"
        for i in data['Listings']:
            #print(i)
            if(int(i['id']) == id):
                listingData = i
            
        return listingData

    def updateListingByID(id, newData):
        with open('flask_app\controllers\db.json','r+') as file:
            file_data = json.load(file)
            for i in file_data['Listings']:
                if(int(i['id']) == int(id)):
                    print("TRUE")
                    i['title'] = newData['title']
                    i['description'] = newData['description']
            #file_data["Listings"].append(i)
            file.seek(0)
            json.dump(file_data, file, indent = 4)

        return -1

    def getUserByID(id):
        f = open('flask_app\controllers\db.json')
        data = json.load(f)
        for i in data['Users']:
            #print(i)
            if(int(i['userID']) == int(id)):
                return i
            
        return "User not found"

    def getUserByEmail(email):
        f = open('flask_app\controllers\db.json')
        data = json.load(f)
        userData = "-1"
        for i in data['Users']:
            #print(i)
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

    def deleteListingByID(ID):

        with open("flask_app\controllers\db.json") as f:
            data = json.load(f)

        idx = 0

        for i in data['Listings']:
            #print(i['id'] + "  ID: " + ID)
            if i['id'] == ID:
                print("TRUE")
                del data['Listings'][idx]
            idx += 1

        with open("flask_app\controllers\db.json", 'w', encoding='utf-8') as fa:
            fa.write(json.dumps(data, indent=4))

    def deleteUserByID():
        return -1
    