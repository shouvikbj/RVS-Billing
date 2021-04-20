from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    make_response,
    jsonify,
)
import os
from db import loginManager, distributorManager, searchManager

app = Flask(__name__, static_url_path="")
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.secret_key = "thisisasecretkey"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")
        resp = loginManager.signupUser(APP_ROOT, email, name, password)
        if resp["status"] == "ok":
            flash(resp["message"], "primary")
            return redirect(url_for("login"))
        else:
            flash(resp["message"], "danger")
            return redirect(url_for("signup"))
    else:
        loggedIn = False
        return render_template("signup.html", loggedIn=loggedIn)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        resp = loginManager.checkAuth(APP_ROOT, email, password)
        if resp["status"] == "ok":
            response = make_response(redirect(url_for("index")))
            response.set_cookie(
                "rvsb", resp["user"]["email"], max_age=60 * 60 * 24 * 365 * 2
            )
            flash(resp["message"], "primary")
            return response
        else:
            flash(resp["message"], "danger")
            return redirect(url_for("login"))
    else:
        loggedIn = False
        return render_template("login.html", loggedIn=loggedIn)


@app.route("/")
def index():
    loggedIn = False
    if request.cookies.get("rvsb"):
        loggedIn = True
        distributorList = distributorManager.getDistributors(
            APP_ROOT, request.cookies.get("rvsb")
        )
        distributorList.reverse()
        return render_template(
            "index.html", loggedIn=loggedIn, distributorList=distributorList
        )
    else:
        return redirect(url_for("login"))


@app.route("/add", methods=["POST", "GET"])
def add():
    loggedIn = False
    if request.method == "POST":
        distributorName = request.form.get("distributorName")
        resp = distributorManager.createDistributor(
            APP_ROOT, request.cookies.get("rvsb"), distributorName
        )
        if resp["status"] == "ok":
            flash(resp["message"], "primary")
            return redirect(url_for("index"))
        else:
            flash(resp["message"], "warning")
            return redirect(url_for("add"))
    else:
        if request.cookies.get("rvsb"):
            loggedIn = True
            return render_template("add.html", loggedIn=loggedIn)
        else:
            return redirect(url_for("login"))


@app.route("/distributor/<id>", methods=["GET"])
def distributor(id):
    loggedIn = False
    if request.cookies.get("rvsb"):
        loggedIn = True
        distributorName = distributorManager.getDistributorName(APP_ROOT, id)
        dataList = distributorManager.getDistributorAccountList(
            APP_ROOT, request.cookies.get("rvsb"), distributorName
        )
        dataList.reverse()
        return render_template(
            "distributor.html",
            loggedIn=loggedIn,
            distributorId=id,
            distributorName=distributorName,
            dataList=dataList,
        )
    else:
        return redirect(url_for("login"))


@app.route("/distributor/<id>/add", methods=["GET", "POST"])
def addDetailsWithinDistributor(id):
    loggedIn = False
    if request.cookies.get("rvsb"):
        if request.method == "POST":
            distributorId = id
            distributorName = distributorManager.getDistributorName(APP_ROOT, id)
            invoiceNumber = request.form.get("invoiceNumber")
            productName = request.form.get("productName")
            date = request.form.get("date")
            billAmount = request.form.get("billAmount")
            actualPayment = request.form.get("actualPayment")
            resp = distributorManager.createBill(
                APP_ROOT,
                request.cookies.get("rvsb"),
                distributorName,
                invoiceNumber,
                productName,
                date,
                billAmount,
                actualPayment,
            )
            if resp["status"] == "ok":
                flash(resp["message"], "success")
            else:
                flash(resp["message"], "danger")
            return redirect(f"/distributor/{distributorId}")
        else:
            loggedIn = True
            distributorId = id
            distributorName = distributorManager.getDistributorName(APP_ROOT, id)
            return render_template(
                "addDistributorBill.html",
                loggedIn=loggedIn,
                distributorId=distributorId,
                distributorName=distributorName,
            )
    else:
        return redirect(url_for("login"))


@app.route("/distributor/<distributorId>/editbill/<billId>", methods=["GET", "POST"])
def editDistributorBill(distributorId, billId):
    loggedIn = False
    if request.cookies.get("rvsb"):
        if request.method == "POST":
            # distributorId = distributorId
            distributorName = distributorManager.getDistributorName(
                APP_ROOT, distributorId
            )
            invoiceNumber = request.form.get("invoiceNumber")
            productName = request.form.get("productName")
            lastUpdated = request.form.get("lastUpdated")
            billAmount = request.form.get("billAmount")
            actualPayment = request.form.get("actualPayment")
            resp = distributorManager.editBill(
                APP_ROOT,
                request.cookies.get("rvsb"),
                distributorName,
                billId,
                invoiceNumber,
                productName,
                lastUpdated,
                billAmount,
                actualPayment,
            )
            if resp["status"] == "ok":
                flash(resp["message"], "success")
                return redirect(f"/distributor/{distributorId}/editbill/{billId}")
            else:
                flash(resp["message"], "danger")
                return redirect(f"/distributor/{distributorId}")
        else:
            loggedIn = True
            # distributorId = distributorId
            distributorName = distributorManager.getDistributorName(
                APP_ROOT, distributorId
            )
            resp = distributorManager.getParticularBill(
                APP_ROOT, request.cookies.get("rvsb"), distributorName, billId
            )
            bill = {}
            if resp["status"] == "ok":
                bill = resp["bill"]
            else:
                flash(resp["message"], "warning")
                return redirect(f"/distributor/{distributorId}")
            return render_template(
                "editDistributorBill.html",
                loggedIn=loggedIn,
                distributorId=distributorId,
                distributorName=distributorName,
                bill=bill,
            )
    else:
        return redirect(url_for("login"))


@app.route("/distributor/<id>/search", methods=["GET", "POST"])
def searchDetailsWithinDistributor(id):
    loggedIn = False
    if request.method == "POST":
        searchText = request.form.get("text")
        distributorId = id
        distributorName = distributorManager.getDistributorName(APP_ROOT, id)
        resp = distributorManager.searchDistributor(
            APP_ROOT, request.cookies.get("rvsb"), distributorName, searchText
        )
        resp.reverse()
        return jsonify(resp)
    else:
        if request.cookies.get("rvsb"):
            loggedIn = True
            distributorId = id
            distributorName = distributorManager.getDistributorName(APP_ROOT, id)
            return render_template(
                "searchDistributor.html",
                loggedIn=loggedIn,
                distributorId=distributorId,
                distributorName=distributorName,
            )
        else:
            return redirect(url_for("login"))


@app.route("/distributor/<id>/showReport", methods=["GET", "POST"])
def showReport(id):
    loggedIn = False
    if request.method == "POST":
        distributorName = distributorManager.getDistributorName(APP_ROOT, id)
        month = request.form.get("month")
        year = request.form.get("year")
        report = distributorManager.generateReport(
            APP_ROOT, request.cookies.get("rvsb"), distributorName, month, year
        )
        totalBillAmount = 0
        totalActualPayment = 0
        for data in report:
            totalBillAmount += int(data["billAmount"])
            totalActualPayment += int(data["actualPayment"])
        total = {
            "name": "Total Summery",
            "billAmount": totalBillAmount,
            "actualPayment": totalActualPayment,
        }
        report.append(total)
        return jsonify(report)
    else:
        if request.cookies.get("rvsb"):
            loggedIn = True
            distributorId = id
            distributorName = distributorManager.getDistributorName(APP_ROOT, id)
            return render_template(
                "report.html",
                loggedIn=loggedIn,
                distributorId=distributorId,
                distributorName=distributorName,
            )
        else:
            return redirect(url_for("login"))


@app.route("/search", methods=["GET"])
def search():
    loggedIn = False
    if request.cookies.get("rvsb"):
        loggedIn = True
        return render_template("search.html", loggedIn=loggedIn)
    else:
        return redirect(url_for("login"))


@app.route("/search/distributor", methods=["POST"])
def searchDistributor():
    searchText = request.form.get("text")
    resp = searchManager.searchDistributor(
        APP_ROOT, request.cookies.get("rvsb"), searchText
    )
    return jsonify(resp)


@app.route("/search/report", methods=["POST"])
def searchReport():
    searchText = request.form.get("text")
    report = searchManager.searchReport(
        APP_ROOT, request.cookies.get("rvsb"), searchText
    )
    totalBillAmount = 0
    totalActualPayment = 0
    for data in report:
        totalBillAmount += int(data["billAmount"])
        totalActualPayment += int(data["actualPayment"])
    total = {
        "name": "Total Summery",
        "billAmount": totalBillAmount,
        "actualPayment": totalActualPayment,
    }
    report.append(total)
    return jsonify(report)


@app.route("/logout")
def logout():
    resp = make_response(redirect(url_for("login")))
    resp.set_cookie("rvsb", expires=0)
    return resp


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=4000)