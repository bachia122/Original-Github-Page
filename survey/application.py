import cs50
import csv
from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Registered millenials
millenials = []


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    if not request.form.get("name"):
        return render_template("error.html", message="missing name")
    if not request.form.get("year"):
        return render_template("error.html", message="missing year")
    """count number of Yes checkbox answers"""
    x = 0
    if request.form.get("q1") == "Yes":
        x += 1
    if request.form.get("q2") == "Yes":
        x += 1
    if request.form.get("q3") == "Yes":
        x += 1
    if request.form.get("q4") == "Yes":
        x += 1
    if request.form.get("q5") == "Yes":
        x += 1
    file = open("survey.csv", "a")
    writer = csv.writer(file)
    writer.writerow((request.form.get("name"), request.form.get("year"), x))
    file.close()
    """if successful"""
    return redirect("/sheet")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    file = open("survey.csv", "r")
    reader = csv.reader(file)
    millenials = list(reader)
    return render_template("table.html", millenials=millenials)