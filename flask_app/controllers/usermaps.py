from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.usermap import Usermap
from flask_app.controllers import dbtalk
import json, random

"""    ROUTES    """

@app.route('/')
def hello_world():
    return 'Hello World!'  # Return the string 'Hello World!' as a response

@app.route('/hello/<name>') # for a route '/hello/____' anything after '/hello/' gets passed as a variable 'name'
def hello(name):
    print(name)
    return "Hello, " + name

@app.route('/map')                           
def map():
    return render_template('map.html')

@app.route('/testcenter/<id>/<userID>')
def testcenter(id, userID):
    id = int(id)

    listingTitle = dbtalk.dbtalk.getListingByID(id)['title']
    listingDescription = dbtalk.dbtalk.getListingByID(id)['description']

    return render_template('testcenter.html', listingTitle = listingTitle, listingDescription = listingDescription)

@app.route('/allListings/<userID>')
def allListings(userID):
    Listings = dbtalk.dbtalk.getAllListings()
    return render_template('allListings.html', Listings = Listings)

@app.route('/login')
def loginPage():
    return render_template('login.html')

@app.route("/loginPOST", methods=['POST', 'GET'])
def loginPOST():

    return redirect("/allListings/0")

@app.route("/new", methods=['POST', 'GET'])
def new():

    #get object to be transferred to JSON for ds.json
    data = {
        "firstName": request.form.get("first_name"),
        "lastName" : request.form.get("last_name"),
        "email" : request.form.get("email"),
        "pw" : request.form.get("password"),
        "userID": str(random.randrange(1, 11000))
    }

    conf = request.form.get("conf")

    #check if password and password confirmation are the same
    if(conf == data['pw']):
        print("TRUE")
    else:
        print("FALSE")

    """implement check for if userID exists and assign new userID"""

    y = json.dumps(data)

    print(y)

    #insert object to JSON file

    with open('flask_app\controllers\db.json','r+') as file:
        file_data = json.load(file)
        file_data["Users"].append(data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)

    return render_template('login.html')




