import json
import os
import nanoid
import copy


def createDistributor(APP_ROOT, creatorEmail, distributorName):
    json_file = open(f"{APP_ROOT}/db/distributor.json", "r")
    distributors = json.load(json_file)
    backup = copy.deepcopy(distributors)
    json_file.close()
    resp = {}
    for distributor in distributors:
        if (
            distributor["creatorEmail"] == creatorEmail
            and distributor["name"] == distributorName
        ):
            resp = {"status": "not-ok", "message": "Distributor already exists!"}
            return resp
    try:
        data = {
            "id": str(nanoid.generate()),
            "creatorEmail": creatorEmail,
            "name": distributorName,
        }
        distributors.append(data)
        json_file = open(f"{APP_ROOT}/db/distributor.json", "w")
        json_file.seek(0)
        json.dump(distributors, json_file, indent=2)
        json_file.close()
        os.makedirs(f"{APP_ROOT}/static/distributors/{creatorEmail}/{distributorName}")
        defaultData = []
        json_file = open(
            f"{APP_ROOT}/static/distributors/{creatorEmail}/{distributorName}/list.json",
            "w",
        )
        json_file.seek(0)
        json.dump(defaultData, json_file, indent=2)
        json_file.close()
        resp = {"status": "ok", "message": "Distributor added!"}
        return resp
    except Exception:
        json_file = open(f"{APP_ROOT}/db/distributor.json", "w")
        json_file.seek(0)
        json.dump(backup, json_file, indent=2)
        json_file.close()
        resp = {"status": "not-ok", "message": "Distributor creation failed!"}
        return resp


def getDistributors(APP_ROOT, creatorEmail):
    json_file = open(f"{APP_ROOT}/db/distributor.json", "r")
    distributors = json.load(json_file)
    json_file.close()
    resp = []
    for distributor in distributors:
        if distributor["creatorEmail"] == creatorEmail:
            resp.append(distributor)
    return resp


def getDistributorName(APP_ROOT, id):
    json_file = open(f"{APP_ROOT}/db/distributor.json", "r")
    distributors = json.load(json_file)
    json_file.close()
    for distributor in distributors:
        if distributor["id"] == id:
            return distributor["name"]


def getDistributorAccountList(APP_ROOT, creatorEmail, distributorName):
    json_file = open(
        f"{APP_ROOT}/static/distributors/{creatorEmail}/{distributorName}/list.json",
        "r",
    )
    data = json.load(json_file)
    json_file.close()
    return data


def createBill(
    APP_ROOT,
    creatorEmail,
    distributorName,
    invoiceNumber,
    productName,
    date,
    billAmount,
    actualPayment,
):
    json_file = open(
        f"{APP_ROOT}/static/distributors/{creatorEmail}/{distributorName}/list.json",
        "r",
    )
    datas = json.load(json_file)
    backup = copy.deepcopy(datas)
    json_file.close()
    resp = {}
    try:
        billId = str(nanoid.generate())
        if invoiceNumber == "":
            invoiceNumber = f"RVSB-{billId}"
        creationDate = f"{date[8:10]}-{date[5:7]}-{date[0:4]}"
        lastUpdated = creationDate
        data = {
            "id": billId,
            "invoiceNumber": invoiceNumber,
            "productName": productName,
            "date": str(creationDate),
            "lastUpdated": str(lastUpdated),
            "billAmount": billAmount,
            "actualPayment": actualPayment,
        }
        datas.append(data)
        json_file = open(
            f"{APP_ROOT}/static/distributors/{creatorEmail}/{distributorName}/list.json",
            "w",
        )
        json_file.seek(0)
        json.dump(datas, json_file, indent=2)
        json_file.close()
        resp = {"status": "ok", "message": "Bill creation successful!"}
        return resp
    except Exception:
        json_file = open(
            f"{APP_ROOT}/static/distributors/{creatorEmail}/{distributorName}/list.json",
            "w",
        )
        json_file.seek(0)
        json.dump(backup, json_file, indent=2)
        json_file.close()
        resp = {"status": "not-ok", "message": "Bill creation failed!"}
        return resp


def getParticularBill(APP_ROOT, creatorEmail, distributorName, billId):
    json_file = open(
        f"{APP_ROOT}/static/distributors/{creatorEmail}/{distributorName}/list.json",
        "r",
    )
    bills = json.load(json_file)
    json_file.close()
    resp = {}
    for bill in bills:
        if bill["id"] == billId:
            resp = {"status": "ok", "bill": bill}
            return resp
    resp = {"status": "not-ok", "message": "Bill not found!"}
    return resp


def editBill(
    APP_ROOT,
    creatorEmail,
    distributorName,
    billId,
    invoiceNumber,
    productName,
    lastUpdatedDate,
    billAmount,
    actualPayment,
):
    json_file = open(
        f"{APP_ROOT}/static/distributors/{creatorEmail}/{distributorName}/list.json",
        "r",
    )
    bills = json.load(json_file)
    backup = copy.deepcopy(bills)
    json_file.close()
    resp = {}
    try:
        lastUpdated = (
            f"{lastUpdatedDate[8:10]}-{lastUpdatedDate[5:7]}-{lastUpdatedDate[0:4]}"
        )
        for bill in bills:
            if bill["id"] == billId:
                bill["invoiceNumber"] = invoiceNumber
                bill["productName"] = productName
                bill["lastUpdated"] = lastUpdated
                bill["billAmount"] = billAmount
                bill["actualPayment"] = actualPayment
                break
        json_file = open(
            f"{APP_ROOT}/static/distributors/{creatorEmail}/{distributorName}/list.json",
            "w",
        )
        json_file.seek(0)
        json.dump(bills, json_file, indent=2)
        json_file.close()
        resp = {"status": "ok", "message": "Bill updation successful!"}
        return resp
    except Exception:
        json_file = open(
            f"{APP_ROOT}/static/distributors/{creatorEmail}/{distributorName}/list.json",
            "w",
        )
        json_file.seek(0)
        json.dump(backup, json_file, indent=2)
        json_file.close()
        resp = {"status": "not-ok", "message": "Bill updation failed!"}
        return resp


def searchDistributor(APP_ROOT, creatorEmail, distributorName, searchText):
    if searchText == "":
        return []
    json_file = open(
        f"{APP_ROOT}/static/distributors/{creatorEmail}/{distributorName}/list.json",
        "r",
    )
    bills = json.load(json_file)
    json_file.close()
    resp = []
    for bill in bills:
        if (
            searchText in bill["invoiceNumber"]
            or searchText.lower() in bill["productName"].lower()
            or searchText.lower() in bill["date"].lower()
            or searchText.lower() in bill["lastUpdated"].lower()
            or searchText.lower() in bill["billAmount"].lower()
            or searchText.lower() in bill["actualPayment"].lower()
        ):
            resp.append(bill)
    return resp


def generateReport(APP_ROOT, creatorEmail, distributorName, month, year):
    monthsList = [
        {"name": "January", "billAmount": 0, "actualPayment": 0},
        {"name": "February", "billAmount": 0, "actualPayment": 0},
        {"name": "March", "billAmount": 0, "actualPayment": 0},
        {"name": "April", "billAmount": 0, "actualPayment": 0},
        {"name": "May", "billAmount": 0, "actualPayment": 0},
        {"name": "June", "billAmount": 0, "actualPayment": 0},
        {"name": "July", "billAmount": 0, "actualPayment": 0},
        {"name": "August", "billAmount": 0, "actualPayment": 0},
        {"name": "September", "billAmount": 0, "actualPayment": 0},
        {"name": "October", "billAmount": 0, "actualPayment": 0},
        {"name": "November", "billAmount": 0, "actualPayment": 0},
        {"name": "December", "billAmount": 0, "actualPayment": 0},
    ]
    if (month == "" and year == "") or (month != "" and year == ""):
        return monthsList
    json_file = open(
        f"{APP_ROOT}/static/distributors/{creatorEmail}/{distributorName}/list.json",
        "r",
    )
    bills = json.load(json_file)
    json_file.close()
    if month == "" and year != "":
        for bill in bills:
            if bill["date"][6:10] == year:
                if bill["date"][3:5] == "01":
                    monthsList[0]["billAmount"] += int(bill["billAmount"])
                    monthsList[0]["actualPayment"] += int(bill["actualPayment"])
                elif bill["date"][3:5] == "02":
                    monthsList[1]["billAmount"] += int(bill["billAmount"])
                    monthsList[1]["actualPayment"] += int(bill["actualPayment"])
                elif bill["date"][3:5] == "03":
                    monthsList[2]["billAmount"] += int(bill["billAmount"])
                    monthsList[2]["actualPayment"] += int(bill["actualPayment"])
                elif bill["date"][3:5] == "04":
                    monthsList[3]["billAmount"] += int(bill["billAmount"])
                    monthsList[3]["actualPayment"] += int(bill["actualPayment"])
                elif bill["date"][3:5] == "05":
                    monthsList[4]["billAmount"] += int(bill["billAmount"])
                    monthsList[4]["actualPayment"] += int(bill["actualPayment"])
                elif bill["date"][3:5] == "06":
                    monthsList[5]["billAmount"] += int(bill["billAmount"])
                    monthsList[5]["actualPayment"] += int(bill["actualPayment"])
                elif bill["date"][3:5] == "07":
                    monthsList[6]["billAmount"] += int(bill["billAmount"])
                    monthsList[6]["actualPayment"] += int(bill["actualPayment"])
                elif bill["date"][3:5] == "08":
                    monthsList[7]["billAmount"] += int(bill["billAmount"])
                    monthsList[7]["actualPayment"] += int(bill["actualPayment"])
                elif bill["date"][3:5] == "09":
                    monthsList[8]["billAmount"] += int(bill["billAmount"])
                    monthsList[8]["actualPayment"] += int(bill["actualPayment"])
                elif bill["date"][3:5] == "10":
                    monthsList[9]["billAmount"] += int(bill["billAmount"])
                    monthsList[9]["actualPayment"] += int(bill["actualPayment"])
                elif bill["date"][3:5] == "11":
                    monthsList[10]["billAmount"] += int(bill["billAmount"])
                    monthsList[10]["actualPayment"] += int(bill["actualPayment"])
                elif bill["date"][3:5] == "12":
                    monthsList[11]["billAmount"] += int(bill["billAmount"])
                    monthsList[11]["actualPayment"] += int(bill["actualPayment"])
        return monthsList

    if month != "" and year != "":
        for bill in bills:
            if bill["date"][6:10] == year and bill["date"][3:5] == month:
                monthsList[(int(month) - 1)]["billAmount"] += int(bill["billAmount"])
                monthsList[(int(month) - 1)]["actualPayment"] += int(
                    bill["actualPayment"]
                )
        return monthsList
