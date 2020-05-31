# Dependencies and Setup
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


# Flask Setup
app = Flask(__name__)

# PyMongo Connection Setup
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# Flask Routes
# Root Route
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Scrape Route
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    mars.update_many({}, {"$set":mars_data}, upsert=True)
    return redirect("/", code=302)

# Define Main Behavior
if __name__ == "__main__":
    app.run()