import json
from turtle import title
class dbtalk:
    def getListingByID(id):
        f = open('flask_app\controllers\db.json')
        data = json.load(f)
        title = "-1"
        for i in data['Listings']:
            print(i)
            if(int(i['id']) == id):
                title = i
            

        return title