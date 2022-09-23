from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.usermap import Usermap
from flask_app.controllers import dbtalk

"""    ROUTES    """

@app.route('/')          # The "@" decorator associates this route with the function immediately following
def hello_world():
    return 'Hello World!'  # Return the string 'Hello World!' as a response

@app.route('/hello/<name>') # for a route '/hello/____' anything after '/hello/' gets passed as a variable 'name'
def hello(name):
    print(name)
    return "Hello, " + name

@app.route('/map')                           
def map():
    # Instead of returning a string, 
    # we'll return the result of the render_template method, passing in the name of our HTML file
    return render_template('map.html')

@app.route('/testcenter/<id>')                           
def testcenter(id):
    id = int(id)

    listingTitle = dbtalk.dbtalk.getListingByID(id)['title']
    listingDescription = dbtalk.dbtalk.getListingByID(id)['description']

    return render_template('testcenter.html', listingTitle = listingTitle, listingDescription = listingDescription)




