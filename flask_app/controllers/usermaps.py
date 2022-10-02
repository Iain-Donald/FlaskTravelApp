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
    currentUser = dbtalk.dbtalk.getUserByID(userID)
    Users = dbtalk.dbtalk.getAllUsers()
    return render_template('allListings.html', Listings = Listings, currentUser = currentUser, Users = Users)

@app.route('/login')
def loginPage():
    return render_template('login.html')

@app.route("/loginPOST", methods=['POST', 'GET'])
def loginPOST():

    # retrieve data from form
    data = {
        "email": request.form.get("email"),
        "pw" : request.form.get("password")
    }

    # get user by email
    retrievedUserByEmail = dbtalk.dbtalk.getUserByEmail(data['email'])

    # default case return back to login page
    redirectString = "/login"

    # check if account exists then return redirect to /allListings/< userID >
    if(retrievedUserByEmail != "-1" and retrievedUserByEmail['pw'] == data['pw']):
        redirectString = "/allListings/" + retrievedUserByEmail['userID']

    return redirect(redirectString)

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

    """implement check for if userID exists and assign new userID"""

    print(json.dumps(data))

    #insert object to JSON file

    if(conf == data['pw']): #check if password and password confirmation are the same
        print("TRUE")
        with open('flask_app\controllers\db.json','r+') as file:
            file_data = json.load(file)
            file_data["Users"].append(data)
            file.seek(0)
            json.dump(file_data, file, indent = 4)
    else:
        print("FALSE")

    return render_template('login.html')




