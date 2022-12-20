from asyncio.windows_events import NULL
from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.controllers import dbtalk
from flask_bcrypt import Bcrypt
import os
from werkzeug.utils import secure_filename
bcrypt = Bcrypt(app)
app.secret_key = 'password123verysecure'
import json, random

"""    ROUTES    """

@app.route("/")
def routeToLogin():
    return redirect("/login")

@app.route('/<testNum>')
def hello_world(testNum):
    returnString = "Hello World! " + testNum
    return returnString  # Return the string 'Hello World!' as a response

@app.route('/map')                           
def map():
    return render_template('map.html')

@app.route('/upImg')
def upImg():
    return render_template('upImg.html')

@app.route('/uploadFile',  methods=("POST", "GET"))
def uploadFile():
    if request.method == 'POST':
        # Upload file flask
        uploaded_img = request.files['uploaded-file']
        # Extracting uploaded data file name
        img_filename = secure_filename(uploaded_img.filename)
        # Upload file to database (defined uploaded folder in static path)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        # Storing uploaded file path in flask session
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)

        return render_template('index_upload_and_show_data_page2.html')

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
    allListingsUserIDs = []
    for key in Listings:
        allListingsUserList.append(dbtalk.dbtalk.getUserByID(key['userID'])['firstName'])
        allListingsUserIDs.append(dbtalk.dbtalk.getUserByID(key['userID'])['userID'])
    if(session['userActive'] != userID):
        return redirect("/login")
    else:
        return render_template('allListings.html', Listings = Listings, currentUser = currentUser, userIDs = allListingsUserIDs, allListingsUserList = allListingsUserList)
    

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

    # default case return back to login page
    redirectString = "/login"

    # get user by email
    retrievedUserByEmail = dbtalk.dbtalk.getUserByEmail(data['email'])
    if(retrievedUserByEmail == "-1"):
        session['loginError'] = "incorrect email or password"
        return redirect(redirectString)

    hashedPass = retrievedUserByEmail['pw']

    """ and bcrypt.check_password_hash(retrievedUserByEmail['pw'].decode('utf8'), data['pw'])"""
    """ and retrievedUserByEmail['pw'] == data['pw'] """

    # check if account exists then return redirect to /allListings/< userID >
    if(retrievedUserByEmail != "-1" and bcrypt.check_password_hash(hashedPass, data['pw'])):
        redirectString = "/allListings/" + retrievedUserByEmail['userID']
        session["userActive"] = retrievedUserByEmail['userID']
        session['loginError'] = ""
        session['newAccountError'] = ""
    else:
        session['loginError'] = "incorrect email or password"

    return redirect(redirectString)

@app.route('/newListing/<userID>')
def newListing(userID):
    if(session['userActive'] != userID):
        return redirect("/login")
    return render_template('newListing.html', userID = userID)


@app.route("/new", methods=['POST', 'GET']) ###     CREATE NEW USER
def new():

    rawPW = request.form.get("password")

    #PW validation

    if(len(rawPW) < 8):
        session['newAccountError'] = "minimum 8 character password"
        return render_template('login.html')

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

@app.route('/editListingPost/<userID>/<listingID>', methods=['POST', 'GET'])
def editListingPost(userID, listingID):

    data = {
        "title": request.form.get("title"),
        "description" : request.form.get("description")
    }

    dbtalk.dbtalk.updateListingByID(listingID, data)

    #print(data['title'] + " " + data['description'])



    redirectString = "/allListings/" + userID
    return redirect(redirectString)