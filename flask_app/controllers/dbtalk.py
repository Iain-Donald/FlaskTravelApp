import json
from turtle import title
class dbtalk:
    def getListingByID(id):
        f = open('db.json')
        data = json.load(f)
        title = "-1"
        for i in data['Listings']:
            print(i.title)
            title = i.title

        return title