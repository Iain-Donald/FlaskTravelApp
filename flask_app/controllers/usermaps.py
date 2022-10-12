from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.controllers import dbtalk
import json, random

"""    ROUTES    """

@app.route('/<testNum>')
def hello_world(testNum):
    returnString = "Hello World! " + testNum
    return returnString  # Return the string 'Hello World!' as a response

@app.route('/map')                           
def map():
    return render_template('map.html')

@app.route('/testcenter/<id>/<userID>')
def testcenter(id, userID):
    id = int(id)

    listingTitle = dbtalk.dbtalk.getListingByID(id)['title']
    listingDescription = dbtalk.dbtalk.getListingByID(id)['description']

    return render_template('testcenter.html', listingTitle = listingTitle, listingDescription = listingDescription)

@app.route('/allListings/<userID>') #     ALL LISTINGS PAGE
def allListings(userID):
    Listings = dbtalk.dbtalk.getAllListings()
    currentUser = dbtalk.dbtalk.getUserByID(userID)
    Users = dbtalk.dbtalk.getAllUsers()
    allListingsUserList = []
    for key in Listings:
        allListingsUserList.append(dbtalk.dbtalk.getUserByID(key['userID'])['firstName'])
    return render_template('allListings.html', Listings = Listings, currentUser = currentUser, Users = Users, allListingsUserList = allListingsUserList)

@app.route('/login')
def loginPage():
    return render_template('login.html')

@app.route("/loginPOST", methods=['POST', 'GET']) ###     LOGIN
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

@app.route('/newListing/<userID>')
def newListing(userID):
    return render_template('newListing.html', userID = userID)


@app.route("/new", methods=['POST', 'GET']) ###     CREATE NEW USER
def new():

    #get object to be transferred to JSON for db.json
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

    if(conf == data['pw']): #check if password and password confirmation match
        print("TRUE")
        with open('flask_app\controllers\db.json','r+') as file:
            file_data = json.load(file)
            file_data["Users"].append(data)
            file.seek(0)
            json.dump(file_data, file, indent = 4)
    else:
        print("FALSE")

    return render_template('login.html')

@app.route("/saveNewListing/<userID>", methods=['POST', 'GET']) ###     SAVE NEW LISTING
def saveNewListing(userID):

    #get object to be transferred to JSON for db.json
    data = {
        "id": str(random.randrange(11001, 22000)),
        "title" : request.form.get("title"),
        "description" : request.form.get("description"),
        "userID" : userID
    }

    """implement check for if userID exists and assign new userID"""

    print(json.dumps(data))

    #insert object to JSON file

    with open('flask_app\controllers\db.json','r+') as file:
        file_data = json.load(file)
        file_data["Listings"].append(data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)

    redirectString = "/allListings/" + userID

    return redirect(redirectString)

@app.route("/deleteListing/<userID>/<ID>", methods=['POST', 'GET']) ###     DELETE LISTING
def deleteListing(userID, ID):

    dbtalk.dbtalk.deleteListingByID(ID)

    redirectString = "/allListings/" + userID
    return redirect(redirectString)


