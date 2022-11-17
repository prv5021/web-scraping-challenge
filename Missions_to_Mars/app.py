#Design a Flash API for Mars Data Scrap
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars


# Flask Setup
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

#Route to render index.html template using data from Mongo
@app.route("/")
def index():
    #access from the database
    mars_data = mongo.db.marsData.find_one()
   
    return render_template("index.html", mars= mars_data)

#scrape route

@app.route("/scrape")
def scrape():
    # identify the collection
    marsTable = mongo.db.marsData

    # drop collection
    mongo.db.marsData.drop()


    #calling the scrape function
    mars_data = scrape_mars.scrape_all()

    #load dictionary into mongoDB
    marsTable.insert_one(mars_data)
    
    return redirect("/")

   
if __name__ == '__main__':
    app.run(debug=True)