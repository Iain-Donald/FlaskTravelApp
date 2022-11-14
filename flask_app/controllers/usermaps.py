from asyncio.windows_events import NULL
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.controllers import dbtalk
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
app.secret_key = 'password123verysecure'
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
    if(session['userActive'] != userID):
        return redirect("/login")
    else:
        return render_template('allListings.html', Listings = Listings, currentUser = currentUser, Users = Users, allListingsUserList = allListingsUserList)
    

@app.route('/login')
def loginPage():
    session['userActive'] = -1
    session['newAccountError'] = ""
    return render_template('login.html')

@app.route("/loginPOST", methods=['POST', 'GET']) ###     LOGIN
def loginPOST():

    # retrieve data from form
    data = {
        "email": request.form.get("email"),
        "pw" : request.form.get("password")
    }

    session['newAccountError'] = ""

    for key in data:
        if(data[key] == ""):
            session['loginError'] = "one or more fields left blank"
            return redirect("/login")

    # get user by email
    retrievedUserByEmail = dbtalk.dbtalk.getUserByEmail(data['email'])
    print(retrievedUserByEmail['pw'])
    hashedPass = retrievedUserByEmail['pw']

    # default case return back to login page
    redirectString = "/login"

    """ and bcrypt.check_password_hash(retrievedUserByEmail['pw'].decode('utf8'), data['pw'])"""
    """ and retrievedUserByEmail['pw'] == data['pw'] """

    # check if account exists then return redirect to /allListings/< userID >
    if(retrievedUserByEmail != "-1" and bcrypt.check_password_hash(hashedPass, data['pw'])):
        redirectString = "/allListings/" + retrievedUserByEmail['userID']
        session["userActive"] = retrievedUserByEmail['userID']
        session['loginError'] = ""
        session['newAccountError'] = ""
    else:
        session['loginError'] = "Incorrect username or password"

    return redirect(redirectString)

@app.route('/newListing/<userID>')
def newListing(userID):
    if(session['userActive'] != userID):
        return redirect("/login")
    return render_template('newListing.html', userID = userID)


@app.route("/new", methods=['POST', 'GET']) ###     CREATE NEW USER
def new():

    rawPW = request.form.get("password")
    pw_hash = bcrypt.generate_password_hash(rawPW).decode('utf-8')

    #get object to be transferred to JSON for db.json
    data = {
        "firstName": request.form.get("first_name"),
        "lastName" : request.form.get("last_name"),
        "email" : request.form.get("email"),
        "pw" : pw_hash,
        "userID": str(random.randrange(1, 11000))
    }

    session['loginError'] = ""

    for key in data:
        if(data[key] == ""):
            session['newAccountError'] = "one or more fields left blank"
            return render_template('login.html')

    conf = request.form.get("conf")

    """implement check for if userID exists and assign new userID"""

    ###print(json.dumps(data))

    #insert object to JSON file

    if(conf == rawPW): #check if password and password confirmation match
        ###print("TRUE")
        session['newAccountError'] = ""
        with open('flask_app\controllers\db.json','r+') as file:
            file_data = json.load(file)
            file_data["Users"].append(data)
            file.seek(0)
            json.dump(file_data, file, indent = 4)
    else:
        session['newAccountError'] = "passwords don't match"

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

    ###print(json.dumps(data))

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


@app.route('/editListing/<userID>/<listingID>')
def editListing(userID, listingID):

    return render_template('editListing.html', userID = userID, listingID = listingID)

@app.route('/editListingPost/<userID>', methods=['POST', 'GET'])
def editListingPost(userID, newData):
    redirectString = "/allListings/" + userID
    return redirect(redirectString)