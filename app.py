from flask import Flask, render_template, request, redirect, url_for
from helper import preprocessing, vectorizer, get_prediction
from logger import logging

app = Flask(__name__)

logging.info('Flask server started')

products = {
    "iphone": {
        "name": "iPhone 15",
        "image": "iphone.webp",
        "reviews": [],
        "positive": 0,
        "negative": 0
    },
    "laptop": {
        "name": "Gaming Laptop",
        "image": "laptop.jpg",
        "reviews": [],
        "positive": 0,
        "negative": 0
    },
    "headphones": {
        "name": "Headphones",
        "image": "headphone.webp",
        "reviews": [],
        "positive": 0,
        "negative": 0
    },
    "camera": {
        "name": "Camera",
        "image": "camera.jpg",
        "reviews": [],
        "positive": 0,
        "negative": 0
    }
}

@app.route("/")
def index():
    return render_template("index.html", products=products)

@app.route("/review/<product_id>", methods=["POST"])
def review(product_id):
    text = request.form["text"]
    logging.info(f"Review: {text}")

    preprocessed = preprocessing(text)
    vectorized = vectorizer(preprocessed)
    prediction = get_prediction(vectorized) 

    if prediction == "positive":
        products[product_id]["positive"] += 1
    else:
        products[product_id]["negative"] += 1

   
    products[product_id]["reviews"].insert(0, {
        "text": text,
        "sentiment": prediction
    })

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
