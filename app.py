from flask import Flask
from flask_pymongo import PyMongo
import scrape_mars

#create an instance of Flask
app = Flask(__name__)

#use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


#route that will scrape the function
@app.route("/scrape")
def scrape():

    #run the scrape function
    mars_data = scrape_mars.scrape()

    #update Mongo database using update and upsert
    mongo.db.collection.update({}, mars_data, upsert=True)


if __name__ == "__main__":
    app.run(debug=True)